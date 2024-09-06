from big_thing_py.core.thing import *
from big_thing_py.core.argument import MXArgument
from big_thing_py.core.mqtt_message import (
    MXExecuteResultMessage,
    MXRegisterResultMessage,
    MXRequestUnregisterMessage,
    MXBinaryValueResultMessage,
    MXRequestRegisterInfoMessage,
    MXExecuteMessage,
    MXUnregisterResultMessage,
    MXHomeResultMessage,
)
from big_thing_py.core.request import MXExecuteRequest, MXInnerExecuteRequest
from big_thing_py.core.ble_advertiser import BLEAdvertiser, BLEErrorCode, DeviceWifiService
from big_thing_py.core.wifi_manager import WiFiManager
from big_thing_py.core.device_model import Objects as DeviceCategory

import ssl
import asyncio
import uvloop
import zeroconf
from zeroconf import ServiceInfo, Zeroconf
import socket

from gmqtt import Client as MQTTClient, Subscription

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


# ASCII Art from https://patorjk.com/software/taag/#p=display&h=1&v=1&f=Big

# ======================================================================== #
#    _____         _____   ____   _      _______  _      _                 #
#   / ____|       |  __ \ |  _ \ (_)    |__   __|| |    (_)                #
#  | (___    ___  | |__) || |_) | _   __ _ | |   | |__   _  _ __    __ _   #
#   \___ \  / _ \ |  ___/ |  _ < | | / _` || |   | '_ \ | || '_ \  / _` |  #
#   ____) || (_) || |     | |_) || || (_| || |   | | | || || | | || (_| |  #
#  |_____/  \___/ |_|     |____/ |_| \__, ||_|   |_| |_||_||_| |_| \__, |  #
#                                     __/ |                         __/ |  #
#                                    |___/                         |___/   #
# ======================================================================== #


class ThingState(Enum):
    RESET = auto()
    NETWORK_SETUP = auto()
    BLE_ADVERTISE = auto()
    BROKER_SETUP = auto()
    NETWORK_CONNECTED = auto()
    BROKER_CONNECTED = auto()
    REGISTERED = auto()
    RUNNING = auto()
    UNREGISTERED = auto()
    RECONNECTED = auto()
    NETWORK_LOST = auto()
    BROKER_LOST = auto()
    NETWORK_RECONNECTED = auto()
    BROKER_RECONNECTED = auto()
    SHUTDOWN = auto()


class MXBigThing:
    MIDDLEWARE_ONLINE_CHECK_INTERVAL = 0.5
    MIDDLEWARE_RECONNECT_TIMEOUT = 30
    CONNECT_RETRY = 3
    ALIVE_CYCLE_SCALER = 2.1
    HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST = [
        MXErrorCode.NO_ERROR,
        MXErrorCode.DUPLICATE,
        MXErrorCode.NOT_FOUND_ERROR,
    ]

    def __init__(
        self,
        name: str = MXThing.DEFAULT_NAME,
        nick_name: str = MXThing.DEFAULT_NAME,
        category: DeviceCategory = DeviceCategory.Undefined,
        desc='',
        version=sdk_version(),
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        is_super: bool = False,
        is_parallel: bool = True,
        is_builtin: bool = False,
        is_manager: bool = False,
        is_matter: bool = False,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_cert_path: str = '',
        ssl_key_path: str = '',
        log_name: str = '',
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        async_log: bool = False,
        append_mac_address: bool = True,
    ):
        # Thing
        self._thing_data: MXThing = MXThing(
            name=name,
            nick_name=nick_name,
            category=category,
            desc=desc,
            version=version,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=is_super,
            is_parallel=is_parallel,
            is_builtin=is_builtin,
            is_manager=is_manager,
            is_matter=is_matter,
        )

        # Log
        self._log_mode = log_mode
        self._log_enable = log_enable
        self._log_name = log_name
        self._async_log = async_log

        # WiFi
        self._ssid = ''
        self._pw = ''

        # MQTT
        self._mqtt_client: MQTTClient = None
        self._ip = ip
        self._port = port
        self._ssl_ca_path = ssl_ca_path
        self._ssl_cert_path = ssl_cert_path
        self._ssl_key_path = ssl_key_path

        # Util
        self._append_mac_address = append_mac_address

        # Queue
        # self._receive_queue: asyncio.Queue = asyncio.Queue()
        self._receive_queue: Dict[MXProtocolType, asyncio.Queue] = {
            MXProtocolType.Base.MT_REQUEST_REGISTER_INFO: asyncio.Queue(),
            MXProtocolType.Base.MT_REQUEST_UNREGISTER: asyncio.Queue(),
            MXProtocolType.Base.MT_RESULT_REGISTER: asyncio.Queue(),
            MXProtocolType.Base.MT_RESULT_UNREGISTER: asyncio.Queue(),
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE: asyncio.Queue(),
            MXProtocolType.Base.MT_EXECUTE: asyncio.Queue(),
            MXProtocolType.Base.MT_IN_EXECUTE: asyncio.Queue(),
            MXProtocolType.WebClient.ME_RESULT_HOME: asyncio.Queue(),
        }

        # Tasks
        self._g_exit = asyncio.Event()
        self._task_list: List[asyncio.Task] = []

        # function_name: MXValue
        # if function executed, MXValue's inner value will be updated
        self._execute_task_list: List[asyncio.Task] = []

        self._loop = None
        self._state = ThingState.RESET
        self._ble_advertiser = BLEAdvertiser(server_name=f'JOI SD {self._thing_data.category.name}')
        self._wifi_manager = WiFiManager()
        self._zeroconf = Zeroconf()
        self._mqtt_mdns_service: ServiceInfo = None
        self._mqtt_ssl_mdns_service: ServiceInfo = None

        if self.is_super and not self.is_parallel:
            raise MXValueError('Super Thing must be parallel')

        self._init_logger()

    def __eq__(self, o: 'MXBigThing') -> bool:
        instance_check = isinstance(o, MXBigThing)
        is_parallel_check = self.is_parallel == o.is_parallel
        is_super_check = self.is_super == o.is_super

        return super().__eq__(o) and instance_check and is_parallel_check and is_super_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_ip'] = self._ip
        state['_port'] = self._port
        state['_ssl_ca_path'] = self._ssl_ca_path
        state['_ssl_cert_path'] = self._ssl_cert_path
        state['_ssl_key_path'] = self._ssl_key_path
        state['_append_mac_address'] = self._append_mac_address

        del state['_log_mode']
        del state['_log_enable']
        del state['_log_name']
        del state['_mqtt_client']
        del state['_g_exit']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._ip = state['_ip']
        self._port = state['_port']
        self._ssl_ca_path = state['_ssl_ca_path']
        self._ssl_cert_path = state['_ssl_cert_path']
        self._ssl_key_path = state['_ssl_key_path']
        self._append_mac_address = state['_append_mac_address']

        self._log_mode = MXPrintMode.ABBR
        self._log_enable = True
        self._log_name = ''
        self._mqtt_client = None
        self._g_exit = asyncio.Event()

    async def _setup(self) -> 'MXBigThing':
        self._ip = convert_url_to_ip(self._ip)
        if not is_valid_ip_address(self._ip) or not 1024 < self._port <= 65535:
            raise MXValueError('Invalid IP address, port number')
        else:
            self._ip = convert_url_to_ip(self._ip)

        if not check_python_version():
            raise MXNotSupportedError('Python version must be 3.7 or higher')

        self._update_thing_id(self.name)

        for service in self.service_list:
            service.add_tag(MXTag(self.name))

        self._mqtt_mdns_service = ServiceInfo(
            type_='_mqtt._tcp.local.',
            name=f'_myssix_thing_{self.name}._mqtt._tcp.local.',
            addresses=[socket.inet_aton(get_local_ip())],
            port=1883,
            properties={'info': 'MySSIX Thing for Non-SSL', 'thing_id': f'JOI SD {self.name}'},
        )
        self._mqtt_ssl_mdns_service = ServiceInfo(
            type_='_mqtt-ssl._tcp.local.',
            name=f'_myssix_thing_{self.name}._mqtt-ssl._tcp.local.',
            addresses=[socket.inet_aton(get_local_ip())],
            port=8883,
            properties={'info': 'MySSIX Thing for SSL', 'thing_id': f'JOI SD {self.name}'},
        )

        self._mqtt_client = MQTTClient(client_id=self.name)
        # FIXME: Later, username and password options must be given by argument of the MXBigThing class
        self._mqtt_client.set_auth_credentials('tester', 'test12')
        self._mqtt_client.set_config({'reconnect_delay': 1})

        self._loop = asyncio.get_running_loop()

        return self

    async def run(self, pre_run: Callable[..., Any] = None, wait_until_pre_run_complete: bool = False):
        await self._setup()

        if asyncio.iscoroutinefunction(pre_run):
            pre_run_task = asyncio.create_task(pre_run())
            if wait_until_pre_run_complete:
                await pre_run_task
        elif callable(pre_run):
            if wait_until_pre_run_complete:
                pre_run()
            else:
                self._loop.run_in_executor(None, pre_run)
        elif pre_run is not None:
            raise ValueError('pre_run must be a callable or a coroutine function')

        await self._main_event_loop()

    async def _wrapup(self):
        try:
            if self._mqtt_client and self._mqtt_client.is_connected:
                self._send_TM_UNREGISTER(self._thing_data)
                # FIXME: Need to wait for the result of unregister
                # recv_msg = await self._receive_queue[MXProtocolType.Base.MT_RESULT_UNREGISTER].get()
                # error = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)

        except Exception as e:
            print_error(e)
            return False
        finally:
            if await self._ble_advertiser.is_advertising():
                await self._ble_advertiser.stop()

            self._unregister_mdns_service()

            if self._mqtt_client and self._mqtt_client.is_connected:
                await self._disconnect_from_broker(disconnect_try=MXBigThing.CONNECT_RETRY)

            MXLOG_DEBUG('Thing Exit', 'red')
            sys.exit(0)

    # ================================================================================================= #
    #   _______  _                            _   ______                    _    _                      #
    #  |__   __|| |                          | | |  ____|                  | |  (_)                     #
    #     | |   | |__   _ __  ___   __ _   __| | | |__  _   _  _ __    ___ | |_  _   ___   _ __   ___   #
    #     | |   | '_ \ | '__|/ _ \ / _` | / _` | |  __|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|  #
    #     | |   | | | || |  |  __/| (_| || (_| | | |   | |_| || | | || (__ | |_ | || (_) || | | |\__ \  #
    #     |_|   |_| |_||_|   \___| \__,_| \__,_| |_|    \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/  #
    # ================================================================================================= #

    async def _preprocessing(self):
        await asyncio.sleep(THREAD_TIME_OUT)

        if self._execute_task_list:
            tasks = await asyncio.wait(self._execute_task_list, return_when=asyncio.FIRST_COMPLETED)
            done_tasks: List[asyncio.Task] = tasks[0]
            for task in done_tasks:
                exception = task.exception()
                if exception:
                    print_error(exception)
                else:
                    execute_request: MXExecuteRequest = task.result()

                    error = self._send_TM_RESULT_EXECUTE(execute_request, self._thing_data)
                    if error == MXErrorCode.NOT_FOUND_ERROR:
                        MXLOG_DEBUG(f'[{get_current_function_name()}] Target function not found!!!', 'red')
                        continue
                    elif error != MXErrorCode.NO_ERROR:
                        MXLOG_DEBUG(f'[{get_current_function_name()}] Send function result failed!!!', 'red')
                        continue

                    dependency_table = self._thing_data.dependency_table
                    dependency_info_list = dependency_table.get(execute_request.result_msg.function_name, [])
                    for dependency_info in dependency_info_list:
                        value: MXValue = dependency_info['value']
                        if dependency_info['set_value_as_result']:
                            target_function = self._get_function(execute_request.result_msg.function_name)
                            set_value: Union[int, float, bool, str] = target_function.return_value
                        else:
                            set_value: Union[int, float, bool, str] = dependency_info['set_value']

                        new_value = await value.update(set_value=set_value)
                        if new_value is None:
                            continue

                        self._send_TM_VALUE_PUBLISH(value)

                        set_value_with_cond = dependency_info['set_value_with_cond']
                        if set_value_with_cond:
                            set_value = set_value_with_cond(new_value)
                        else:
                            set_value: Union[int, float, bool, str] = dependency_info['set_value']
                            new_value = await value.update(set_value=set_value)
                            if new_value is None:
                                continue

            self._execute_task_list = [task for task in self._execute_task_list if not task.done()]

    async def _RESET_state_process(self):
        if self.is_builtin or self.is_manager:
            self.next_state = ThingState.BROKER_SETUP
        else:
            self.next_state = ThingState.BLE_ADVERTISE

    async def _BLE_ADVERTISE_state_process(self):
        # BLE Advertise
        await self._ble_advertiser.start(self.name)
        if not await self._ble_advertiser.is_advertising():
            MXLOG_DEBUG(f'BLE Advertiser start failed...', 'red')
            await self._ble_advertiser.stop()
            self.next_state = ThingState.RESET
            return

        # Save WiFi, Broker info
        MXLOG_DEBUG(f'Wait for WiFi credentials from BLE...', 'yellow')
        self._ssid, self._pw, broker, ble_error = await self._ble_advertiser.wait_until_wifi_credentials_set(timeout=None)
        self._ip = broker.split(':')[0]
        self._port = int(broker.split(':')[1])

        if ble_error != BLEErrorCode.NO_ERROR:
            MXLOG_DEBUG(f'Something getting wrong while BLE setup! error code: {ble_error}', 'red')
            await self._ble_advertiser.stop()
            self.next_state = ThingState.RESET
            return

        self.next_state = ThingState.NETWORK_SETUP

    async def _NETWORK_SETUP_state_process(self):
        # WiFi Connect
        self._wifi_manager.ssid = self._ssid
        self._wifi_manager.password = self._pw

        wifi_connect_try = MXBigThing.CONNECT_RETRY
        while wifi_connect_try > 0:
            await self._wifi_manager.connect()
            if self._wifi_manager.check_connection() and self._wifi_manager.network_reachable(self._ip, self._port):
                MXLOG_DEBUG(f'WiFi connection success. SSID: {self._wifi_manager.get_connected_wifi_ssid()}', 'green')
                self.next_state = ThingState.BROKER_SETUP
                return
            else:
                if wifi_connect_try > 0:
                    MXLOG_DEBUG(f'Connect to SSID {self._wifi_manager.ssid} failed... (try: {wifi_connect_try})', 'yellow')
                    wifi_connect_try -= 1
                else:
                    MXLOG_DEBUG(f'WiFi connection failed... Go back to BLE setup.', 'red')
                    wifi_connect_try = MXBigThing.CONNECT_RETRY
                    self.next_state = ThingState.RESET
                    return

    async def _BROKER_SETUP_state_process(self):
        if not await self._connect_to_broker(MXBigThing.CONNECT_RETRY):
            MXLOG_DEBUG(f'Connect to broker failed... Check broker host and port -> {self._ip}:{self._port}', 'red')
            self.next_state = ThingState.SHUTDOWN
            return

        # Setup avahi mDNS service
        if not self._register_mdns_service():
            MXLOG_DEBUG(f'Register mDNS service failed... Retry to register mDNS service.', 'red')
            self._unregister_mdns_service()
            self.next_state = ThingState.BROKER_SETUP
            return

        self.next_state = ThingState.BROKER_CONNECTED

    async def _BROKER_CONNECTED_state_process(self):
        # Prepare to register
        self._subscribe_init_topic_list(self._thing_data)
        self._subscribe_service_topic_list(self._thing_data)

        if self.is_builtin or self.is_manager:
            MXLOG_DEBUG(f'Run builtin or plugin Thing', 'yellow')
            self._send_TM_REGISTER(self._thing_data)

            recv_msg = await self._receive_queue[MXProtocolType.Base.MT_RESULT_REGISTER].get()
            result = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data, state_change=False)
            if not result in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE, MXErrorCode.INVALID_REQUEST]:
                self._unsubscribe_all_topic_list(self._thing_data)
                self.next_state = ThingState.SHUTDOWN
            else:
                self.next_state = ThingState.REGISTERED
        else:
            # Ready to receive TM_REQUEST_REGISTER_INFO
            self._ble_advertiser.write_characteristic(
                DeviceWifiService.ErrorCodeCharacteristic().uuid, bytearray(str(BLEErrorCode.NO_ERROR.value).encode())
            )

            recv_msg = await self._receive_queue[MXProtocolType.Base.MT_REQUEST_REGISTER_INFO].get()
            self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)

            await self._ble_advertiser.stop()

            recv_msg = await self._receive_queue[MXProtocolType.Base.MT_RESULT_REGISTER].get()
            result = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data, state_change=False)
            if not result in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE, MXErrorCode.INVALID_REQUEST]:
                self._unsubscribe_all_topic_list(self._thing_data)
                self.next_state = ThingState.SHUTDOWN
            else:
                self.next_state = ThingState.REGISTERED

    async def _REGISTERED_state_process(self):
        self.next_state = ThingState.RUNNING

    async def _RUNNING_state_process(self):
        # MQTT receive handling
        if not self._receive_queue_empty():
            recv_msg = await self._receive_queue_get()
            error = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)
            if not error in MXBigThing.HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST:
                MXLOG_DEBUG(f'[{get_current_function_name()}] MQTT Message handling failed', 'red')

        # Value publish handling
        current_time = get_current_datetime()
        for value in self.value_list:
            if not value.is_initialized:
                await value.update()
                self._send_TM_VALUE_PUBLISH(value)
            # NOTE (thsvkd): If Thing is not Manager of Staff, I think event-based value feature is not needed...
            # elif current_time - value.last_update_time > value.cycle and value.cycle != 0:
            elif current_time - value.last_update_time > value.cycle:
                new_value = await value.update()
                if new_value is None:
                    continue

                self._send_TM_VALUE_PUBLISH(value)

        # Alive handling
        if current_time - self.last_alive_time > self.alive_cycle / MXBigThing.ALIVE_CYCLE_SCALER:
            self._send_TM_ALIVE(self._thing_data)

    async def _UNREGISTERED_state_process(self):
        if await self._ble_advertiser.is_advertising():
            await self._ble_advertiser.stop()

        self._unregister_mdns_service()

        # NOTE (thsvkd): Wait for finish previous MQTT tasks... It needs to be modified to wait based on conditions, not fixed time.
        await asyncio.sleep(0.1)
        if self._mqtt_client and self._mqtt_client.is_connected:
            await self._disconnect_from_broker(disconnect_try=MXBigThing.CONNECT_RETRY)

        # TODO: need to disconnect from wifi router

        self.next_state = ThingState.RESET

    async def _RECONNECTED_state_process(self):
        # TODO: do something
        pass

    async def _NETWORK_LOST_state_process(self):
        # WiFi Connect
        self._wifi_manager.ssid = self._ssid
        self._wifi_manager.password = self._pw

        wifi_connect_try = MXBigThing.CONNECT_RETRY
        while wifi_connect_try > 0:
            await self._wifi_manager.connect()
            if self._wifi_manager.check_connection() and self._wifi_manager.network_reachable(self._ip, self._port):
                MXLOG_DEBUG(f'WiFi connection success. SSID: {self._wifi_manager.get_connected_wifi_ssid()}', 'green')
                self.next_state = ThingState.BROKER_LOST
                return
            else:
                if wifi_connect_try > 0:
                    MXLOG_DEBUG(f'Connect to SSID {self._wifi_manager.ssid} failed... (try: {wifi_connect_try})', 'yellow')
                    wifi_connect_try -= 1
                else:
                    MXLOG_DEBUG(f'WiFi connection failed... Go back to BLE setup.', 'red')
                    wifi_connect_try = MXBigThing.CONNECT_RETRY
                    self.next_state = ThingState.RESET
                    return

    async def _BROKER_LOST_state_process(self):
        if self._mqtt_client.is_connected:
            self.next_state = ThingState.BROKER_RECONNECTED
        else:
            self.next_state = ThingState.BROKER_LOST
            await asyncio.sleep(1)

    async def _NETWORK_RECONNECTED_state_process(self):
        # TODO: do something
        pass

    async def _BROKER_RECONNECTED_state_process(self):
        get_home_msg = self._thing_data.generate_get_home_message().mqtt_message()
        result_home_topic = MXProtocolType.WebClient.ME_RESULT_HOME.value % '+'
        self._subscribe(result_home_topic)

        current_time = get_current_datetime()
        while get_current_datetime() - current_time < MXBigThing.MIDDLEWARE_RECONNECT_TIMEOUT:
            self._publish(get_home_msg.topic, get_home_msg.payload)
            try:
                recv_msg = self._receive_queue[MXProtocolType.WebClient.ME_RESULT_HOME].get_nowait()
                self._handle_mqtt_message(recv_msg, target_thing=self._thing_data, state_change=False)

                # Auto subscription restore feature
                subscriptions: List[Subscription] = self._mqtt_client.subscriptions
                for subscription in subscriptions:
                    self._mqtt_client.resubscribe(subscription)

                self._send_TM_ALIVE(self._thing_data)
                self.next_state = ThingState.BROKER_CONNECTED
                break
            except asyncio.QueueEmpty:
                await asyncio.sleep(MXBigThing.MIDDLEWARE_ONLINE_CHECK_INTERVAL)
        else:
            if self.is_builtin or self.is_manager:
                self.next_state = ThingState.SHUTDOWN
            else:
                MXLOG_DEBUG(f'Middleware is offline... Go back to BLE setup.', 'red')
                self.next_state = ThingState.BLE_ADVERTISE

    async def _main_event_loop(self):
        while not self._g_exit.is_set():
            try:
                await self._preprocessing()

                if self._state == ThingState.RESET:
                    await self._RESET_state_process()
                elif self._state == ThingState.BLE_ADVERTISE:
                    await self._BLE_ADVERTISE_state_process()
                elif self._state == ThingState.NETWORK_SETUP:
                    await self._NETWORK_SETUP_state_process()
                elif self._state == ThingState.BROKER_SETUP:
                    await self._BROKER_SETUP_state_process()
                elif self._state == ThingState.BROKER_CONNECTED:
                    await self._BROKER_CONNECTED_state_process()
                elif self._state == ThingState.REGISTERED:
                    await self._REGISTERED_state_process()
                elif self._state == ThingState.RUNNING:
                    await self._RUNNING_state_process()
                elif self._state == ThingState.UNREGISTERED:
                    await self._UNREGISTERED_state_process()
                elif self._state == ThingState.RECONNECTED:
                    await self._RECONNECTED_state_process()
                elif self._state == ThingState.NETWORK_LOST:
                    await self._NETWORK_LOST_state_process()
                elif self._state == ThingState.BROKER_LOST:
                    await self._BROKER_LOST_state_process()
                elif self._state == ThingState.NETWORK_RECONNECTED:
                    await self._NETWORK_RECONNECTED_state_process()
                elif self._state == ThingState.BROKER_RECONNECTED:
                    await self._BROKER_RECONNECTED_state_process()
                elif self._state == ThingState.SHUTDOWN:
                    await self._wrapup()
                else:
                    MXLOG_DEBUG(f'Unexpected state!!! state: {self._state}', 'red')
                    self.next_state = ThingState.SHUTDOWN
            except BaseException as e:
                if isinstance(e, KeyboardInterrupt):
                    MXLOG_DEBUG('KeyboardInterrupt Exit', 'red')
                    await self._wrapup()
                elif isinstance(e, asyncio.CancelledError):
                    MXLOG_DEBUG('asyncio.CancelledError Exit', 'red')
                    await self._wrapup()
                elif isinstance(e, zeroconf._exceptions.NonUniqueNameException):
                    self._unregister_mdns_service()
                    self.next_state = ThingState.BROKER_SETUP
                elif isinstance(e, ConnectionRefusedError):
                    MXLOG_DEBUG(f'Connect to broker failed... broker - {self._ip}:{self._port}', 'red')
                elif isinstance(e, ConnectionResetError):
                    MXLOG_DEBUG(f'Disconnect from broker failed... broker - {self._ip}:{self._port}', 'red')
                else:
                    print_error(e)
                    raise e

    # ======================================================================================================================= #
    #  _    _                    _  _         __  __   ____  _______  _______   __  __                                        #
    # | |  | |                  | || |       |  \/  | / __ \|__   __||__   __| |  \/  |                                       #
    # | |__| |  __ _  _ __    __| || |  ___  | \  / || |  | |  | |      | |    | \  / |  ___  ___  ___   __ _   __ _   ___    #
    # |  __  | / _` || '_ \  / _` || | / _ \ | |\/| || |  | |  | |      | |    | |\/| | / _ \/ __|/ __| / _` | / _` | / _ \   #
    # | |  | || (_| || | | || (_| || ||  __/ | |  | || |__| |  | |      | |    | |  | ||  __/\__ \\__ \| (_| || (_| ||  __/   #
    # |_|  |_| \__,_||_| |_| \__,_||_| \___| |_|  |_| \___\_\  |_|      |_|    |_|  |_| \___||___/|___/ \__,_| \__, | \___|   #
    #                                                                                                         __/ |           #
    #                                                                                                         |___/           #
    # ======================================================================================================================= #

    def _handle_mqtt_message(self, msg: MQTTMessage, target_thing: MXThing, state_change: bool = True) -> MXErrorCode:
        topic = decode_MQTT_message(msg)[0]
        protocol = MXProtocolType.get(topic)

        if protocol == MXProtocolType.Base.MT_REQUEST_REGISTER_INFO:
            error = self._handle_MT_REQUEST_REGISTER_INFO(msg, target_thing=target_thing)
        elif protocol == MXProtocolType.Base.MT_REQUEST_UNREGISTER:
            error = self._handle_MT_REQUEST_UNREGISTER(msg, target_thing=target_thing)
        elif protocol == MXProtocolType.Base.MT_RESULT_REGISTER:
            error = self._handle_MT_RESULT_REGISTER(msg, target_thing=target_thing)
            if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
                # NOTE (thsvkd): MT_RESULT_REGISTER topic also use as a trigger for sending the current
                # Value to the middleware regardless of the cycle. If the MT_RESULT_REGISTER topic comes
                # while running after being registered, it is implemented to work as a trigger for value
                # publish by initializing the values.
                if self._state in [ThingState.RUNNING, ThingState.REGISTERED]:
                    for value in target_thing.value_list:
                        value.is_initialized = False

                self.next_state = ThingState.REGISTERED if state_change else self._state
            elif error == MXErrorCode.INVALID_DESTINATION:
                self.next_state = ThingState.REGISTERED if state_change else self._state
            elif error == MXErrorCode.FAIL:
                MXLOG_DEBUG(
                    f'{PrintTag.ERROR} Register failed... Thing {self.name} register packet is not valid. error code: {error}',
                    'red',
                )
                self.next_state = ThingState.SHUTDOWN if state_change else self._state
            elif error == MXErrorCode.INVALID_REQUEST:
                MXLOG_DEBUG(f'Receive unexpected packet... Drop it. topic: {topic}', 'magenta')
            else:
                MXLOG_DEBUG(
                    f'{PrintTag.ERROR} Register failed... Thing {self.name} register packet is not valid. error code: {error}',
                    'red',
                )
                self.next_state = ThingState.SHUTDOWN if state_change else self._state
        elif protocol == MXProtocolType.Base.MT_RESULT_UNREGISTER:
            error = self._handle_MT_RESULT_UNREGISTER(msg, target_thing=target_thing)
            if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
                self.next_state = ThingState.UNREGISTERED if state_change else self._state
            elif error == MXErrorCode.INVALID_DESTINATION:
                self.next_state = ThingState.UNREGISTERED if state_change else self._state
            elif error == MXErrorCode.FAIL:
                MXLOG_DEBUG(
                    f'{PrintTag.ERROR} Unregister failed...',
                    'red',
                )
            elif error == MXErrorCode.INVALID_REQUEST:
                MXLOG_DEBUG(f'Receive unexpected packet... Drop it. topic: {topic}', 'magenta')
            else:
                MXLOG_DEBUG(
                    f'{PrintTag.ERROR} Unregister failed... Thing {self.name} Unregister packet is not valid. error code: {error}',
                    'red',
                )
                self.next_state = ThingState.SHUTDOWN if state_change else self._state
        elif protocol == MXProtocolType.Base.MT_RESULT_BINARY_VALUE:
            error = self._handle_MT_RESULT_BINARY_VALUE(msg, target_thing=target_thing)
        elif protocol in [MXProtocolType.Base.MT_EXECUTE, MXProtocolType.Base.MT_IN_EXECUTE]:
            error = self._handle_MT_EXECUTE(msg, target_thing=target_thing)
        # for Auto Re-register feature
        elif protocol == MXProtocolType.WebClient.ME_RESULT_HOME:
            error = self._handle_ME_HOME_RESULT(msg)

            result_home_topic = MXProtocolType.WebClient.ME_RESULT_HOME.value % '+'
            if error == MXErrorCode.NO_ERROR:
                self._unsubscribe(result_home_topic)
                self.next_state = ThingState.REGISTERED if state_change else self._state
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected topic! topic: {topic}')
            error = MXErrorCode.FAIL

        return error

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    def _handle_MT_REQUEST_REGISTER_INFO(self, msg: MQTTMessage, target_thing: MXThing) -> MXErrorCode:
        request_register_info_msg = MXRequestRegisterInfoMessage(msg)

        if request_register_info_msg.topic_error or request_register_info_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        middleware_name = request_register_info_msg.middleware_name
        MXLOG_DEBUG(f'Receive register request from Middleware {middleware_name}! Send Register packet.', 'green')

        target_thing.request_client_id = request_register_info_msg.client_id
        self._send_TM_REGISTER(target_thing)
        return MXErrorCode.NO_ERROR

    def _handle_MT_REQUEST_UNREGISTER(self, msg: MQTTMessage, target_thing: MXThing) -> MXErrorCode:
        request_unregister_msg = MXRequestUnregisterMessage(msg)

        if request_unregister_msg.topic_error or request_unregister_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        middleware_name = request_unregister_msg.middleware_name
        MXLOG_DEBUG(f'Receive unregister request from Middleware {middleware_name}! Send Unregister packet.', 'green')

        target_thing.request_client_id = request_unregister_msg.client_id
        self._send_TM_UNREGISTER(target_thing)
        return MXErrorCode.NO_ERROR

    def _handle_MT_RESULT_REGISTER(self, msg: MQTTMessage, target_thing: MXThing) -> MXErrorCode:
        register_result_msg = MXRegisterResultMessage(msg)
        error = register_result_msg.error

        if register_result_msg.topic_error or register_result_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        if target_thing.name != register_result_msg.thing_name:
            # MXLOG_DEBUG(
            #     f'[{get_current_function_name()}] Wrong payload arrive... {target_thing.name} should be arrive, not {register_result_msg.thing_name}'
            # )
            return MXErrorCode.INVALID_DESTINATION

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(
                f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {target_thing.name} {colored("register", "green")} success!'
            )
            target_thing.middleware_name = register_result_msg.middleware_name
            for service in target_thing.service_list:
                service.middleware_name = target_thing.middleware_name
                service.thing_name = target_thing.name
            self._subscribe_service_topic_list(target_thing)
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Thing {target_thing.name} register packet is not valid. error code: {register_result_msg.error}',
                'red',
            )
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Register failed... Unexpected error occurred!!! error code: {register_result_msg.error}',
                'red',
            )

        return error

    def _handle_MT_RESULT_UNREGISTER(self, msg: MQTTMessage, target_thing: MXThing) -> MXErrorCode:
        unregister_result_msg = MXUnregisterResultMessage(msg)
        error = unregister_result_msg.error

        if unregister_result_msg.topic_error or unregister_result_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        if target_thing.name != unregister_result_msg.thing_name:
            # MXLOG_DEBUG(
            #     f'[{get_current_function_name()}] Wrong payload arrive... {target_thing.name} should be arrive, not {unregister_result_msg.thing_name}',
            #     'red',
            # )
            return MXErrorCode.INVALID_DESTINATION

        if error in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE]:
            MXLOG_DEBUG(
                f'{PrintTag.GOOD if error == MXErrorCode.NO_ERROR else PrintTag.DUP} Thing {target_thing.name} {colored("unregister", "red")} success!'
            )
            self._unsubscribe_all_topic_list(self._thing_data)
        elif error == MXErrorCode.FAIL:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Thing {target_thing.name} unregister packet is not valid. error code: {unregister_result_msg.error}',
                'red',
            )
        else:
            MXLOG_DEBUG(
                f'{PrintTag.ERROR} Unregister failed... Unexpected error occurred!!! error code: {unregister_result_msg.error}',
                'red',
            )

        return error

    def _handle_MT_EXECUTE(self, msg: MQTTMessage, target_thing: MXThing) -> Tuple[asyncio.Task, MXErrorCode]:
        execute_msg = MXExecuteMessage(msg)
        if execute_msg.topic_error or execute_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        target_function = target_thing.get_function(execute_msg.function_name)
        if not target_function:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Target function not found! - topic: {decode_MQTT_message(msg)[0]}')
            return MXErrorCode.NOT_FOUND_ERROR
        if target_thing.name != execute_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {target_thing.name} should be arrive, not {execute_msg.thing_name}',
                'red',
            )
            return MXErrorCode.INVALID_REQUEST
        if execute_msg.topic_error or execute_msg.payload_error:
            MXLOG_DEBUG(f'[{get_current_function_name()}] execute_msg error! - topic: {decode_MQTT_message(msg)[0]}{execute_msg.topic_error}')
            return MXErrorCode.INVALID_REQUEST

        execute_protocol = MXProtocolType.get(execute_msg.topic)
        execute_result_msg_input = dict(
            function_name=target_function.name,
            thing_name=target_function.thing_name,
            middleware_name=target_function.middleware_name,
            scenario=execute_msg.scenario,
            client_id=execute_msg.client_id,
            request_ID=execute_msg.request_ID,
            return_type=target_function.return_type,
            return_value=None,
        )
        if execute_protocol == MXProtocolType.Base.MT_EXECUTE:
            execute_request = MXExecuteRequest(
                trigger_msg=execute_msg,
                result_msg=MXExecuteResultMessage(
                    **execute_result_msg_input,
                    action_type=MXActionType.EXECUTE,
                ),
            )
        elif execute_protocol == MXProtocolType.Base.MT_IN_EXECUTE:
            execute_request = MXInnerExecuteRequest(
                trigger_msg=execute_msg,
                result_msg=MXExecuteResultMessage(
                    **execute_result_msg_input,
                    action_type=MXActionType.INNER_EXECUTE,
                ),
            )
        else:
            raise MXValueError('Invalid protocol type')

        # 서로의 arg_list가 일치하는 지 확인한다.
        if not self._compare_arg_list(target_function.arg_list, list(execute_request.trigger_msg.tuple_arguments())):
            self._send_TM_RESULT_EXECUTE(execute_request, self._thing_data)
            return MXErrorCode.EXECUTE_ARG_FAIL

        # 중복된 시나리오로부터 온 실행 요청이면 -4 에러코드를 보낸다.
        if execute_request.trigger_msg.scenario in target_function.running_scenario_list:
            execute_request.result_msg.error = MXErrorCode.DUPLICATE
            self._send_TM_RESULT_EXECUTE(execute_request, self._thing_data)
            return MXErrorCode.DUPLICATE

        # 병렬실행이 가능한지 옵션을 살펴보고, 이후에 실행 중인지 살펴본다.
        if target_thing.is_parallel:
            cur_time = get_current_datetime(TimeFormat.DATETIME2)
            MXLOG_DEBUG(f'[FUNC RUN REQUEST] Request function {target_function.name} run by {execute_msg.scenario} at [{cur_time}]', 'green')
            task = asyncio.create_task(target_function.execute(execute_request))
        elif not target_function._running:
            task = asyncio.create_task(target_function.execute(execute_request))
        else:
            execute_request.result_msg.error = MXErrorCode.FAIL
            self._send_TM_RESULT_EXECUTE(execute_request, self._thing_data)

        self._execute_task_list.append(task)

        return MXErrorCode.NO_ERROR

    def _handle_MT_RESULT_BINARY_VALUE(self, msg: MQTTMessage, target_thing: MXThing) -> bool:
        binary_value_result_msg = MXBinaryValueResultMessage(msg)

        if binary_value_result_msg.topic_error or binary_value_result_msg.payload_error:
            return MXErrorCode.INVALID_REQUEST

        if target_thing.name != binary_value_result_msg.thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Wrong payload arrive... {target_thing.name} should be arrive, not {binary_value_result_msg.thing_name}',
                'red',
            )
            return MXErrorCode.INVALID_REQUEST

        for value in target_thing.value_list:
            if value.name == binary_value_result_msg.value_name and value.type == MXType.BINARY:
                value.binary_sending = False
                return MXErrorCode.NO_ERROR
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Value {binary_value_result_msg.value_name} does not exist!!!', 'red')
            return MXErrorCode.NOT_FOUND_ERROR

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    def _send_TM_REGISTER(self, thing_data: MXThing) -> None:
        self._subscribe_init_topic_list(thing_data)

        register_msg = thing_data.generate_register_message()
        if not register_msg:
            raise Exception('TM_REGISTER packet error')

        register_mqtt_msg = register_msg.mqtt_message()
        self._publish(register_mqtt_msg.topic, register_mqtt_msg.payload)

    def _send_TM_UNREGISTER(self, thing_data: MXThing):
        unregister_msg = thing_data.generate_unregister_message()
        if not unregister_msg:
            raise Exception('TM_UNREGISTER packet error')

        unregister_mqtt_msg = unregister_msg.mqtt_message()
        self._publish(unregister_mqtt_msg.topic, unregister_mqtt_msg.payload)

    def _send_TM_ALIVE(self, thing_data: MXThing):
        alive_msg = thing_data.generate_alive_message()
        alive_mqtt_msg = alive_msg.mqtt_message()
        self._publish(alive_mqtt_msg.topic, alive_mqtt_msg.payload)
        thing_data.last_alive_time = get_current_datetime()

    def _send_TM_VALUE_PUBLISH(self, value: MXValue) -> None:
        value_publish_msg = value.generate_value_publish_message()
        value_publish_mqtt_msg = value_publish_msg.mqtt_message()

        if value.type == MXType.BINARY:
            value.binary_sending = True
        self._publish(value_publish_mqtt_msg.topic, value_publish_mqtt_msg.payload)

    def _send_TM_RESULT_EXECUTE(self, execute_request: Union[MXExecuteRequest, MXInnerExecuteRequest], thing_data: MXThing) -> MXErrorCode:
        target_function = thing_data.get_function(execute_request.result_msg.function_name)
        if target_function is None:
            return MXErrorCode.NOT_FOUND_ERROR

        execute_result_msg = target_function.generate_execute_result_message(execute_request)
        execute_result_mqtt_msg = execute_result_msg.mqtt_message()
        self._publish(execute_result_mqtt_msg.topic, execute_result_mqtt_msg.payload)
        return MXErrorCode.NO_ERROR

    # ================
    #  __  __  ______
    # |  \/  ||  ____|
    # | \  / || |__
    # | |\/| ||  __|
    # | |  | || |____
    # |_|  |_||______|
    # ================

    # for Auto Re-register feature
    def _handle_ME_HOME_RESULT(self, msg: MQTTMessage) -> MXErrorCode:
        execute_msg = MXHomeResultMessage(msg)
        if 'location' in execute_msg.payload:
            MXLOG_DEBUG(f'Middleware detected!!!')
            return MXErrorCode.NO_ERROR
        else:
            return MXErrorCode.FAIL

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _get_function(self, function_name: str) -> MXFunction:
        return self._thing_data.get_function(function_name)

    def _receive_queue_empty(self):
        for queue in self._receive_queue.values():
            if not queue.empty():
                return False
        return True

    def _receive_queue_get(self):
        for queue in self._receive_queue.values():
            if not queue.empty():
                return queue.get()
        return None

    def _subscribe_init_topic_list(self, thing_data: MXThing) -> None:
        topic_list = [
            MXProtocolType.Base.MT_REQUEST_REGISTER_INFO.value % thing_data.name,
            MXProtocolType.Base.MT_REQUEST_UNREGISTER.value % thing_data.name,
            MXProtocolType.Base.MT_RESULT_REGISTER.value % thing_data.name,
            MXProtocolType.Base.MT_RESULT_UNREGISTER.value % thing_data.name,
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE.value % thing_data.name,
        ]

        for topic in topic_list:
            self._subscribe(topic)

    def _subscribe_service_topic_list(self, thing_data: MXThing):
        topic_list = []

        for function in thing_data.function_list:
            topic_list += [
                MXProtocolType.Base.MT_EXECUTE.value % (function.name, thing_data.name, '+', '+'),
                (MXProtocolType.Base.MT_EXECUTE.value % (function.name, thing_data.name, '', '')).rstrip('/'),
                MXProtocolType.Base.MT_IN_EXECUTE.value % (function.name, thing_data.name),
            ]

        for topic in topic_list:
            self._subscribe(topic)

    def _unsubscribe_service_topic_list(self):
        topic_list = []

        subscriptions: List[Subscription] = self._mqtt_client.subscriptions
        for topic in [sub.topic for sub in subscriptions]:
            if (
                MXProtocolType.Base.MT_EXECUTE.get_prefix() in topic
                or MXProtocolType.Base.MT_IN_EXECUTE.get_prefix() in topic
                or MXProtocolType.Base.MT_EXECUTE.get_prefix() in topic
            ):
                topic_list.append(topic)

        for topic in topic_list:
            self._unsubscribe(topic)

    def _unsubscribe_all_topic_list(self, target_thing: MXThing) -> None:
        subscriptions: List[Subscription] = self._mqtt_client.subscriptions
        for topic in [sub.topic for sub in subscriptions if target_thing.name in sub.topic]:
            self._unsubscribe(topic)

    def _convert_arg_list(self, arg_list: List[Union[MXArgument, Union[int, float, str, bool, BinaryBase64]]]) -> List[MXType]:
        # In case of arg_list is list of MXArgument
        if isinstance(arg_list, list) and all([isinstance(arg, MXArgument) for arg in arg_list]):
            return [arg.type for arg in arg_list]
        # In case of arg_list is list of {int, float, str, bool, BinaryBase64}
        elif isinstance(arg_list, list) and all([isinstance(arg, (int, float, str, bool, BinaryBase64)) for arg in arg_list]):
            return [self._convert_arg(arg).type for arg in arg_list]
        else:
            raise MXTypeError(f'arg_list must be list of MXArgument or list of int, float, str, bool: {arg_list}')

    def _convert_arg(self, arg: Union[int, float, str, bool, BinaryBase64]) -> MXArgument:
        if isinstance(arg, bool):
            return MXArgument(name='converted_argument', type=MXType.BOOL, bound=(0, 1))
        elif isinstance(arg, int):
            return MXArgument(name='converted_argument', type=MXType.INTEGER, bound=(-sys.maxsize - 1, sys.maxsize))
        elif isinstance(arg, float):
            return MXArgument(name='converted_argument', type=MXType.DOUBLE, bound=(-sys.maxsize - 1, sys.maxsize))
        elif isinstance(arg, str):
            if is_base64(arg):
                return MXArgument(name='converted_argument', type=MXType.BINARY)
            else:
                return MXArgument(name='converted_argument', type=MXType.STRING)
        else:
            raise MXTypeError(f'arg must be int, float, str, bool, BinaryBase64: {arg}')

    def _compare_arg_list(
        self,
        arg_list1: List[Union[MXArgument, Union[int, float, str, bool]]],
        arg_list2: List[Union[MXArgument, Union[int, float, str, bool]]],
    ):
        arg_type_list1 = self._convert_arg_list(arg_list1)
        arg_type_list2 = self._convert_arg_list(arg_list2)

        if len(arg_type_list1) != len(arg_type_list2):
            MXLOG_DEBUG(f'Not matched arg_list length: {len(arg_type_list1)} != {len(arg_type_list2)}', 'red')
            return False

        for arg_type1, arg_type2 in zip(arg_type_list1, arg_type_list2):
            if arg_type1 in [MXType.INTEGER, MXType.DOUBLE] and arg_type2 in [MXType.INTEGER, MXType.DOUBLE]:
                pass
            elif arg_type1 != arg_type2:
                MXLOG_DEBUG(f'Not matched arg_list type: {arg_type1} != {arg_type2}', 'red')
                return False
        else:
            return True

    def _print_packet(
        self, topic: Union[str, bytes], payload: Union[str, bytes], direction: Direction, mode: MXPrintMode = MXPrintMode.FULL, pretty: bool = False
    ) -> str:
        if isinstance(topic, bytes):
            topic = topic.decode()
        if isinstance(payload, bytes):
            payload = dict_to_json_string(json_string_to_dict(payload.decode()), ensure_ascii=False)

        topic_template = MXProtocolType.get(topic)
        if not topic_template:
            MXLOG_DEBUG(f'[print_packet] Unknown topic!!! topic : {topic}')

        topic_indicator = '_'.join([topic_token for topic_token in topic_template.value.split('/') if topic_token != '%s'])
        payload = prune_payload(payload=dict_to_json_string(dict_object=payload, pretty=pretty), mode=mode)

        MXLOG_DEBUG(f'[{topic_indicator:20}][{direction.value}] topic: {topic} payload: {payload}')

    def add_service(self, service: MXService) -> 'MXThing':
        return self._thing_data.add_service(service)

    def dict(self) -> dict:
        return self._thing_data.dict()

    def add_dependency(
        self,
        function: MXFunction,
        value: MXValue,
        set_value: Union[int, float, bool, str] = None,
        set_value_as_result: bool = False,
    ) -> None:
        self._thing_data.add_dependency(function=function, value=value, set_value=set_value, set_value_as_result=set_value_as_result)

    #### MQTT utils ####

    async def _connect_to_broker(self, connect_try: int) -> bool:
        # Set SSL options
        if self._check_ssl_enable():
            MXLOG_DEBUG('Connect with SSL...', 'green')
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(certfile=self._ssl_cert_path, keyfile=self._ssl_key_path)
            ssl_context.load_verify_locations(cafile=self._ssl_ca_path)
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            # ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # TLSv1.2 이상만 사용
            ssl_context.check_hostname = False
        else:
            ssl_context = False
            MXLOG_DEBUG('[WARN] Connect without SSL...', 'yellow')

        # Broker Connect
        while connect_try:
            try:
                if self._mqtt_client.is_connected or await self._connect(self._ip, self._port, ssl=ssl_context):
                    return True

                await asyncio.sleep(THREAD_TIME_OUT * 10)
                MXLOG_DEBUG(f'Connect to Broker {self._ip}:{self._port} failed... (try: {connect_try})', 'yellow')
                connect_try -= 1
            except BaseException as e:
                if isinstance(e, ConnectionRefusedError) or isinstance(e, ConnectionResetError):
                    await asyncio.sleep(THREAD_TIME_OUT * 10)
                    MXLOG_DEBUG(f'Connect to Broker {self._ip}:{self._port} failed... (try: {connect_try})', 'yellow')
                    connect_try -= 1
                else:
                    raise e
        else:
            MXLOG_DEBUG(f'Broker connection failed...', 'red')
            connect_try = MXBigThing.CONNECT_RETRY
            return False

    async def _disconnect_from_broker(self, disconnect_try: int) -> bool:
        # Broker Disconnect
        while disconnect_try:
            try:
                await self._disconnect()
                if not self._mqtt_client.is_connected:
                    return True

                await asyncio.sleep(THREAD_TIME_OUT * 10)
                MXLOG_DEBUG(f'Disconnect to Broker {self._ip}:{self._port} failed... (try: {disconnect_try})', 'yellow')
                disconnect_try -= 1
            except BaseException as e:
                if isinstance(e, ConnectionResetError):
                    await asyncio.sleep(THREAD_TIME_OUT * 10)
                    MXLOG_DEBUG(f'Disconnect to Broker {self._ip}:{self._port} failed... (try: {disconnect_try})', 'yellow')
                    disconnect_try -= 1
                else:
                    raise e
        else:
            MXLOG_DEBUG(f'Broker disconnection failed... Go back to BLE setup.', 'red')
            disconnect_try = MXBigThing.CONNECT_RETRY
            return False

    async def _connect(self, ip: str, port: int, ssl: Union[ssl.SSLContext, bool], timeout: float = 1) -> bool:
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_disconnect = self._on_disconnect
        # self._mqtt_client.on_publish = self._on_publish
        self._mqtt_client.on_subscribe = self._on_subscribe
        self._mqtt_client.on_unsubscribe = self._on_unsubscribe
        self._mqtt_client.on_message = self._on_message

        try:
            await asyncio.wait_for(self._mqtt_client.connect(ip, port, ssl=ssl), timeout=timeout)
        except asyncio.TimeoutError:
            return False

        return self._mqtt_client.is_connected

    async def _disconnect(self):
        await self._mqtt_client.disconnect()

    def _subscribe(self, topic: str, qos: int = 0):
        subscriptions: List[Subscription] = self._mqtt_client.subscriptions
        if not topic in [sub.topic for sub in subscriptions]:
            rc = self._mqtt_client.subscribe(topic, qos=qos)

        return True

    def _unsubscribe(self, topic: str):
        subscriptions: List[Subscription] = self._mqtt_client.subscriptions
        if topic in [sub.topic for sub in subscriptions]:
            rc = self._mqtt_client.unsubscribe(topic)
            MXLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} {topic}')

        return True

    def _publish(self, topic: Union[str, bytes], payload: Union[str, bytes], qos: int = 0) -> int:
        self._print_packet(topic=topic, payload=payload, direction=Direction.PUBLISH, mode=self._log_mode)

        if isinstance(topic, str):
            topic = topic.encode()
        if isinstance(payload, str):
            payload = payload.encode()

        self._mqtt_client.publish(topic, payload, qos=qos)

    def _init_logger(self):
        if self._log_enable:
            MXLogger(logger_type=LoggerType.ALL, logging_mode=LogLevel.DEBUG, async_mode=self._async_log).start()
        else:
            MXLogger(logger_type=LoggerType.OFF, logging_mode=LogLevel.DEBUG, async_mode=self._async_log).start()

    def _check_ssl_enable(self) -> bool:
        if not self._ssl_ca_path and not self._ssl_cert_path and not self._ssl_key_path:
            return False
        if not os.path.exists(self._ssl_ca_path):
            raise MXNotFoundError(f'SSL CA file not found. invalid path: {self._ssl_ca_path}')
        elif not os.path.exists(self._ssl_cert_path):
            raise MXNotFoundError(f'SSL Cert file not found. invalid path: {self._ssl_cert_path}')
        elif not os.path.exists(self._ssl_key_path):
            raise MXNotFoundError(f'SSL Key file not found.. invalid path: {self._ssl_key_path}')
        else:
            return True

    def _update_thing_id(self, name: str, interface: str = None) -> None:
        self.name = self._thing_data.generate_thing_id(name, self._append_mac_address, interface=interface)

    def _register_mdns_service(self) -> bool:
        try:
            self._zeroconf.register_service(self._mqtt_mdns_service)
            self._zeroconf.register_service(self._mqtt_ssl_mdns_service)
            return True
        except zeroconf.NonUniqueNameException as e:
            return True
        except Exception as e:
            print_error(e)
            return False

    def _unregister_mdns_service(self) -> None:
        self._zeroconf.unregister_service(self._mqtt_mdns_service)
        self._zeroconf.unregister_service(self._mqtt_ssl_mdns_service)

    # ===================================================================================
    # ___  ___ _____  _____  _____   _____         _  _  _                   _
    # |  \/  ||  _  ||_   _||_   _| /  __ \       | || || |                 | |
    # | .  . || | | |  | |    | |   | /  \/  __ _ | || || |__    __ _   ___ | | __ ___
    # | |\/| || | | |  | |    | |   | |     / _` || || || '_ \  / _` | / __|| |/ // __|
    # | |  | |\ \/' /  | |    | |   | \__/\| (_| || || || |_) || (_| || (__ |   < \__ \
    # \_|  |_/ \_/\_\  \_/    \_/    \____/ \__,_||_||_||_.__/  \__,_| \___||_|\_\|___/
    # ===================================================================================

    def _on_connect(self, client: MQTTClient, flags, rc, properties):
        if rc == 0:
            MXLOG_DEBUG(f'{PrintTag.CONNECT} Connect to Host: {self._ip}:{self._port}')
        else:
            MXLOG_DEBUG(f'{PrintTag.ERROR} Bad connection... Returned code: {rc}', 'red')

    def _on_disconnect(self, client: MQTTClient, packet, exc=None):
        self.next_state = ThingState.BROKER_LOST
        MXLOG_DEBUG(f'{PrintTag.DISCONNECT} Disconnect from broker {self._ip}:{self._port}')

    def _on_subscribe(self, client: MQTTClient, mid: int, qos, properties):
        subscriptions: List[Subscription] = self._mqtt_client.get_subscriptions_by_mid(mid)
        for sub in subscriptions:
            MXLOG_DEBUG(f'{PrintTag.SUBSCRIBE} {sub.topic}')

    def _on_unsubscribe(self, client: MQTTClient, mid: int, qos):
        subscriptions: List[Subscription] = self._mqtt_client.get_subscriptions_by_mid(mid)
        for sub in subscriptions:
            MXLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} {sub.topic}')

    # def _on_publish(self, client: MQTTClient, userdata: MQTTMessage, mid):
    #     pass

    async def _on_message(self, client: MQTTClient, topic, payload, qos, properties):
        # topic, payload = decode_MQTT_message(msg)
        self._print_packet(topic=topic, payload=payload, direction=Direction.RECEIVED, mode=self._log_mode)
        msg = encode_MQTT_message(topic, payload)

        protocol = MXProtocolType.get(topic)
        if protocol in [
            MXProtocolType.Base.MT_REQUEST_REGISTER_INFO,
            MXProtocolType.Base.MT_REQUEST_UNREGISTER,
            MXProtocolType.Base.MT_RESULT_REGISTER,
            MXProtocolType.Base.MT_RESULT_UNREGISTER,
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE,
            MXProtocolType.Base.MT_EXECUTE,
            MXProtocolType.Base.MT_IN_EXECUTE,
            MXProtocolType.WebClient.ME_RESULT_HOME,
        ]:
            await self._receive_queue[protocol].put(msg)
        else:
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unexpected topic! topic: {topic}')

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    @property
    def function_list(self) -> List[MXFunction]:
        return sorted(
            [service for service in self._thing_data.service_list if isinstance(service, MXFunction) and not service.name.startswith('__')],
            key=lambda x: x.name,
        )

    @property
    def value_list(self) -> List[MXValue]:
        return sorted([service for service in self._thing_data.service_list if isinstance(service, MXValue)], key=lambda x: x.name)

    @property
    def service_list(self) -> List[MXService]:
        return sorted(self._thing_data.service_list, key=lambda x: x.name)

    @property
    def name(self) -> str:
        return self._thing_data.name

    @property
    def nick_name(self) -> str:
        return self._thing_data.nick_name

    @property
    def middleware_name(self) -> str:
        return self._thing_data.middleware_name

    @property
    def last_alive_time(self) -> float:
        return self._thing_data.last_alive_time

    @property
    def alive_cycle(self) -> float:
        return self._thing_data.alive_cycle

    @property
    def subscribed_topic_set(self) -> Set[str]:
        return self._thing_data.subscribed_topic_set

    @property
    def is_super(self) -> bool:
        return self._thing_data.is_super

    @property
    def is_parallel(self) -> bool:
        return self._thing_data.is_parallel

    @property
    def is_builtin(self) -> bool:
        return self._thing_data.is_builtin

    @property
    def is_manager(self) -> bool:
        return self._thing_data.is_manager

    @property
    def is_matter(self) -> bool:
        return self._thing_data.is_matter

    @property
    def current_state(self):
        return self._state

    def get_log_mode(self) -> MXPrintMode:
        return self._log_mode

    def get_log_enable(self) -> bool:
        return self._log_enable

    def get_log_name(self) -> str:
        return self._log_enable

    def get_ip(self) -> str:
        return self._ip

    def get_port(self) -> int:
        return self._port

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    @name.setter
    def name(self, name: str) -> None:
        self._thing_data.name = name
        for service in self._thing_data.service_list:
            service.thing_name = name

    @nick_name.setter
    def nick_name(self, nick_name: str) -> None:
        self._thing_data.nick_name = nick_name

    @middleware_name.setter
    def middleware_name(self, middleware_name: str) -> None:
        self._thing_data.middleware_name = middleware_name
        for service in self._thing_data.service_list:
            service.middleware_name = middleware_name

    @last_alive_time.setter
    def last_alive_time(self, last_alive_time: float) -> None:
        self._thing_data.last_alive_time = last_alive_time

    @alive_cycle.setter
    def alive_cycle(self, alive_cycle: float) -> None:
        self._thing_data.alive_cycle = alive_cycle

    @subscribed_topic_set.setter
    def subscribed_topic_set(self, subscribed_topic_set: Set[str]) -> None:
        self._thing_data.subscribed_topic_set = subscribed_topic_set

    @is_super.setter
    def is_super(self, is_super: bool) -> bool:
        self._thing_data.is_super = is_super

    @is_parallel.setter
    def is_parallel(self, is_parallel: bool) -> bool:
        self._thing_data.is_parallel = is_parallel

    @is_builtin.setter
    def is_builtin(self, is_builtin: bool) -> bool:
        self._thing_data.is_builtin = is_builtin

    @is_manager.setter
    def is_manager(self, is_manager: bool) -> bool:
        self._thing_data.is_manager = is_manager

    @is_matter.setter
    def is_matter(self, is_matter: bool) -> bool:
        self._thing_data.is_matter = is_matter

    @current_state.setter
    def next_state(self, state: ThingState):
        self._state = state
        MXLOG_DEBUG(f'Current state: {self._state}', 'cyan')

    def set_log_mode(self, mode: MXPrintMode) -> None:
        self._log_mode = mode

    def set_log_enable(self, enable: bool) -> None:
        self._log_enable = enable

    def set_log_name(self, name: str) -> None:
        self._log_name = name

    def set_ip(self, ip: str) -> None:
        self._ip = ip

    def set_port(self, port: int) -> None:
        self._port = port
