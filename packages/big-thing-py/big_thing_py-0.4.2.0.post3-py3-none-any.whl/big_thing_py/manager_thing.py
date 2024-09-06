from big_thing_py.big_thing import *
from big_thing_py.staff_thing import MXStaffThing
from big_thing_py.manager import *
from big_thing_py.core.service_model import Objects as Skill
import uuid
import pwd


class MXManagerThing(MXBigThing, metaclass=ABCMeta):
    DEFAULT_STAFF_THING_STORE_PATH = 'staff_thing_info.json'

    def __init__(
        self,
        name: str = MXThing.DEFAULT_NAME,
        nick_name: str = MXThing.DEFAULT_NAME,
        category=DeviceCategory.ManagerThing,
        desc='',
        version=sdk_version(),
        service_list: List[MXService] = [],
        alive_cycle: float = 60,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_cert_path: str = '',
        ssl_key_path: str = '',
        log_name: str = '',
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        append_mac_address: bool = True,
    ):
        super().__init__(
            name=name,
            nick_name=nick_name,
            category=category,
            desc=desc,
            version=version,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=False,
            is_parallel=True,
            is_builtin=False,
            is_manager=True,
            is_matter=False,
            ip=ip,
            port=port,
            ssl_ca_path=ssl_ca_path,
            ssl_cert_path=ssl_cert_path,
            ssl_key_path=ssl_key_path,
            log_name=log_name,
            log_enable=log_enable,
            log_mode=log_mode,
            append_mac_address=append_mac_address,
        )

        self._staff_thing_list: List[MXStaffThing] = []
        self._subscribe_event_server_task: asyncio.Task = None

    @override
    async def _setup(self):
        default_tag_list = [MXTag('manager')]

        value_list = []
        function_list = [
            MXFunction(
                func=self._discover,
                name='discover',
                category=Skill.manager.Functions.discover,
                tag_list=default_tag_list,
                return_type=MXType.STRING,
                arg_list=[
                    # MXArgument(name='timeout', type=MXType.DOUBLE, bound=(0, 60)),
                ],
                exec_time=30,
                timeout=60,
            ),
            MXFunction(
                func=self._add_thing,
                name='add_thing',
                category=Skill.manager.Functions.add_thing,
                tag_list=default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[
                    MXArgument(name='staff_thing_info', type=MXType.STRING, bound=(0, 999999)),
                    MXArgument(name='client_id', type=MXType.STRING, bound=(0, 999999)),
                ],
                exec_time=30,
                timeout=60,
            ),
            MXFunction(
                func=self._delete_thing,
                name='delete_thing',
                category=Skill.manager.Functions.delete_thing,
                tag_list=default_tag_list,
                return_type=MXType.BOOL,
                arg_list=[
                    MXArgument(name='staff_thing_info', type=MXType.STRING, bound=(0, 999999)),
                    MXArgument(name='client_id', type=MXType.STRING, bound=(0, 999999)),
                ],
                exec_time=30,
                timeout=60,
            ),
        ]

        await super()._setup()
        self._subscribe_event_server_task = asyncio.create_task(self._subscribe_event_server())

        for service in value_list + function_list:
            self.add_service(service)

    @override
    async def _wrapup(self):
        try:
            if self._mqtt_client and self._mqtt_client.is_connected:
                self._send_TM_UNREGISTER(self._thing_data)
                for thing in self._staff_thing_list:
                    self._send_TM_UNREGISTER(thing)
                # FIXME: Need to wait for the result of unregister
                # recv_msg = await self._receive_queue[MXProtocolType.Base.MT_RESULT_UNREGISTER].get()
                # error = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)

            return True
        except Exception as e:
            print_error(e)
            return False
        finally:
            if await self._ble_advertiser.is_advertising():
                await self._ble_advertiser.stop()

            self._unregister_mdns_service()

            if self._mqtt_client and self._mqtt_client.is_connected:
                await self._disconnect_from_broker(disconnect_try=MXBigThing.CONNECT_RETRY)

            await self._close_event_server()
            self._subscribe_event_server_task.cancel()

            MXLOG_DEBUG('Thing Exit', 'red')
            sys.exit(0)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    @override
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

                    error_list = []
                    for thing in self._whole_thing_list:
                        if find_class_in_hierarchy(thing, MXManagerThing) or type(thing) is MXThing:
                            target_thing = self._thing_data
                        elif find_class_in_hierarchy(thing, MXStaffThing):
                            target_thing = thing
                        else:
                            raise ValueError(f'Unknown type instance: {type(thing)}')

                        if target_thing.name != execute_request.result_msg.thing_name:
                            continue

                        error = self._send_TM_RESULT_EXECUTE(execute_request, target_thing)
                        error_list.append(error)
                        if error != MXErrorCode.NO_ERROR:
                            continue

                        dependency_table = target_thing.dependency_table
                        dependency_info_list = dependency_table.get(execute_request.result_msg.function_name, [])
                        for dependency_info in dependency_info_list:
                            value: MXValue = dependency_info['value']
                            if dependency_info['set_value_as_result']:
                                target_function = thing.get_function(execute_request.result_msg.function_name)
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

                    if all([error == MXErrorCode.NOT_FOUND_ERROR for error in error_list]):
                        MXLOG_DEBUG(f'[{get_current_function_name()}] Target function not found!!!', 'red')
                    elif any([not error in MXBigThing.HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST for error in error_list]):
                        MXLOG_DEBUG(f'[{get_current_function_name()}] Send function result failed!!!', 'red')

            self._execute_task_list = [task for task in self._execute_task_list if not task.done()]

    @override
    async def _BROKER_CONNECTED_state_process(self):
        # Prepare to register Manager Thing
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

        # Prepare to register Staff Things
        loaded_staff_thing_list = await self._load_staff_thing_info()
        for loaded_staff_thing in loaded_staff_thing_list:
            latest_staff_thing = await self._check_thing_exist(loaded_staff_thing)
            if not latest_staff_thing:
                MXLOG_WARN(f'[{get_current_function_name()}] Staff Thing {loaded_staff_thing.name} is offline', 'red')
                loaded_staff_thing.is_alive = False
                continue

            latest_staff_thing.is_alive = True
            latest_staff_thing.last_alive_time = get_current_datetime()

            # If staff thing's info is updated, store the updated info
            if latest_staff_thing.name == loaded_staff_thing.name and latest_staff_thing.nick_name == loaded_staff_thing.nick_name:
                MXLOG_DEBUG(f'Load staff thing {loaded_staff_thing.name} completed!', 'cyan')
            else:
                MXLOG_DEBUG(
                    f'Update staff thing\'s nick name {loaded_staff_thing.name} completed! {loaded_staff_thing.nick_name} -> {latest_staff_thing.nick_name}',
                    'cyan',
                )
                self._delete_staff_thing_info(loaded_staff_thing)
                self._store_staff_thing_info(latest_staff_thing)

            await self._add_staff_thing(latest_staff_thing)

            self._subscribe_init_topic_list(latest_staff_thing)
            self._subscribe_service_topic_list(latest_staff_thing)

            MXLOG_DEBUG(f'Run builtin or plugin Thing', 'yellow')
            self._send_TM_REGISTER(latest_staff_thing)

            recv_msg = await self._receive_queue[MXProtocolType.Base.MT_RESULT_REGISTER].get()
            self._handle_mqtt_message(recv_msg, target_thing=latest_staff_thing, state_change=False)
            if not result in [MXErrorCode.NO_ERROR, MXErrorCode.DUPLICATE, MXErrorCode.INVALID_REQUEST]:
                self._unsubscribe_all_topic_list(latest_staff_thing)
                self.next_state = ThingState.SHUTDOWN
            else:
                self.next_state = ThingState.REGISTERED

    @override
    async def _RUNNING_state_process(self):
        # MQTT receive handling
        if not self._receive_queue_empty():
            recv_msg = await self._receive_queue_get()

            # # MQTT receive handling(Manager Thing)
            # error = self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)
            # if error == MXErrorCode.INVALID_DESTINATION:

            # if not error in MXBigThing.HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST:
            #     MXLOG_DEBUG(f'[{get_current_function_name()}] MQTT Message handling failed', 'red')

            # MQTT receive handling(Staff Thing)
            for thing in self._whole_thing_list:
                if isinstance(thing, MXManagerThing):
                    thing_data = thing._thing_data
                    state_change = True
                elif isinstance(thing, MXStaffThing):
                    thing_data = thing
                    state_change = False

                target_thing_name = topic_split(decode_MQTT_message(recv_msg)[0])[-1]
                if target_thing_name != thing_data.name:
                    continue

                error = self._handle_mqtt_message(recv_msg, target_thing=thing_data, state_change=state_change)
                if not error in MXBigThing.HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] MQTT Message handling failed', 'red')

        # Value publish & Alive handling (Manager Thing)
        current_time = get_current_datetime()
        for value in self.value_list:
            if not value.is_initialized:
                await value.update()
                self._send_TM_VALUE_PUBLISH(value)
            # NOTE (thsvkd): cycle == 0 mean, value is event-based
            elif current_time - value.last_update_time > value.cycle and value.cycle != 0:
                new_value = await value.update()
                if new_value is None:
                    continue

                self._send_TM_VALUE_PUBLISH(value)

        if current_time - self.last_alive_time > self.alive_cycle / MXBigThing.ALIVE_CYCLE_SCALER:
            self._send_TM_ALIVE(self._thing_data)

        # Value publish & Alive handling (Staff Thing)
        for thing in self._staff_thing_list:
            for value in thing.value_list:
                if not thing.is_alive:
                    continue

                if not value.is_initialized:
                    await value.update()
                    self._send_TM_VALUE_PUBLISH(value)
                # NOTE (thsvkd): cycle == 0 mean, value is event-based
                elif current_time - value.last_update_time > value.cycle and value.cycle != 0:
                    new_value = await value.update()
                    if new_value is None:
                        continue

                    self._send_TM_VALUE_PUBLISH(value)

            if current_time - thing.last_alive_time > thing.alive_cycle / MXBigThing.ALIVE_CYCLE_SCALER:
                if await self._check_thing_exist(thing):
                    if not thing.is_alive:
                        MXLOG_DEBUG(f'Staff Thing {thing.name} is online', 'cyan')
                        thing.is_alive = True
                        self._send_TM_REGISTER(thing)

                    self._send_TM_ALIVE(thing)
                else:
                    if thing.is_alive:
                        MXLOG_DEBUG(f'Staff Thing {thing.name} is offline', 'red')
                        thing.is_alive = False
                        self._send_TM_UNREGISTER(thing)

    @override
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
                # Send alive for staff things
                for staff_thing in self._staff_thing_list:
                    self._send_TM_ALIVE(staff_thing)
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

    # ===========================
    #            _____   _____
    #     /\    |  __ \ |_   _|
    #    /  \   | |__) |  | |
    #   / /\ \  |  ___/   | |
    #  / ____ \ | |      _| |_
    # /_/    \_\|_|     |_____|
    # ===========================

    @abstractmethod
    def _extract_staff_thing_info(self, staff_thing_info: dict) -> dict:
        '''
        staff thing 정보를 추출하는 함수

        Args:
            staff_thing_info (dict): staff thing의 정보를 담고 있는 딕셔너리

        Returns:
            dict: 추출된 staff thing 정보를 담고 있는 딕셔너리
        '''
        pass

    @abstractmethod
    def _create_staff(self, staff_thing_info: dict) -> Union[MXStaffThing, None]:
        '''
        _scan_staff_thing() 함수를 통해 수집된 staff thing 정보를 바탕으로 staff thing을 생성하는 함수.
        만약 스캔하는 것만으로 완벽한 staff thing의 정보를 수집할 수 없다면, staff thing의 register 메시지를 받아 처리하는
        _handle_REGISTER_staff_message() 함수에서 staff thing을 self._staff_thing_list에서 찾아 정보를 추가할 수 있다.

        Args:
            staff_thing_info (dict): staff thing의 정보를 담고 있는 딕셔너리

        Returns:
            staff_thing(MXStaffThing): 생성한 staff thing 인스턴스
        '''
        pass

    @abstractmethod
    async def _scan_staff_thing(self, timeout: float) -> Tuple[List[dict], str]:
        '''
        지속적으로 staff thing을 발견하여 정보를 수집하여 반환하는 함수.
        timeout을 지정하여 한 번 staff thing을 검색하는데 소요될 시간을 지정할 수 있다.

        Args:
            timeout (float): staff thing을 검색하는데 소요될 시간

        Returns:
            List[dict]: staff thing의 정보를 담고 있는 리스트
        '''
        pass

    @abstractmethod
    async def _check_thing_exist(self, staff_thing: MXStaffThing) -> Union[bool, MXStaffThing]:
        '''
        staff thing이 실제로 존재하는 지 검사하는 함수

        Args:
            staff_thing (MXStaffThing): staff thing의 정보를 담고 있는 문자열

        Returns:
            Union[bool, MXStaffThing]: staff thing가 존재하는 경우 staff thing 인스턴수를, 존재하지 않는 경우 False를 반환
        '''
        pass

    @abstractmethod
    async def _add_thing__(self, staff_thing_info_string: str, client_id: str) -> Union[MXStaffThing, None]:
        '''
        staff thing을 추가하는 함수.

        Args:
            staff_thing_info_string (str): staff thing의 정보를 담고 있는 문자열
            client_id (str): staff thing을 등록 요청하는 클라이언트의 ID

        Returns:
            dict: staff thing 추가 결과 딕셔너리
        '''
        pass

    @abstractmethod
    async def _delete_thing__(self, staff_thing_info_string: str, client_id: str) -> Union[MXStaffThing, None]:
        '''
        staff thing을 삭제하는 함수.

        Args:
            staff_thing_info_string (str): staff thing의 정보를 담고 있는 문자열
            client_id (str): staff thing을 삭제 요청하는 클라이언트의 ID

        Returns:
            dict: staff thing 삭제 결과 딕셔너리
        '''
        pass

    @abstractmethod
    async def _subscribe_event_server(self) -> asyncio.Task:
        '''
        event server를 구독하는 함수

        Args: None

        Returns:
            asyncio.Task: event server를 구독하는 task
        '''
        pass

    @abstractmethod
    async def _close_event_server(self) -> None:
        '''
        event server를 종료하는 함수

        Args: None

        Returns: None
        '''
        pass

    async def _add_thing(self, staff_thing_info_string: str, client_id: str) -> dict:
        target_staff_thing = await self._add_thing__(staff_thing_info_string, client_id)
        if target_staff_thing:
            self._store_staff_thing_info(target_staff_thing)
            return dict(thing=target_staff_thing.name, error=MXErrorCode.NO_ERROR.value)
        else:
            return dict(thing='', error=MXErrorCode.FAIL.value)

    async def _delete_thing(self, staff_thing_info_string: str, client_id: str) -> dict:
        target_staff_thing = await self._delete_thing__(staff_thing_info_string, client_id)
        if target_staff_thing:
            self._delete_staff_thing_info(target_staff_thing)
            return dict(thing=target_staff_thing.name, error=MXErrorCode.NO_ERROR.value)
        else:
            return dict(thing='', error=MXErrorCode.FAIL.value)

    async def _discover(self) -> str:
        staff_thing_list, error_string = await self._scan_staff_thing()
        if staff_thing_list:
            discovered_things = dict(things=staff_thing_list, error=MXErrorCode.NO_ERROR.value, error_string='')
        else:
            discovered_things = dict(things=[], error=MXErrorCode.FAIL.value, error_string=error_string)

        return dict_to_json_string(discovered_things)

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _get_thing(self, thing_name: str) -> MXThing:
        for thing in self._whole_thing_list:
            if thing.name == thing_name:
                return thing

    async def _add_staff_thing(self, staff_thing: MXStaffThing) -> MXStaffThing:
        if staff_thing in self._staff_thing_list:
            MXLOG_WARN(f'[{get_current_function_name()}] Staff Thing {staff_thing.name} is already added')
        else:
            if not await staff_thing.setup():
                raise ValueError(f'[{get_current_function_name()}] Staff Thing {staff_thing.name} setup failed')

            staff_thing.is_alive = True
            self._staff_thing_list.append(staff_thing)

        return staff_thing

    async def _delete_staff_thing(self, staff_thing: MXStaffThing) -> bool:
        if not staff_thing in self._staff_thing_list:
            MXLOG_WARN(f'[{get_current_function_name()}] Staff Thing {staff_thing.name} is not exist')

        if not await staff_thing.wrapup():
            raise ValueError(f'[{get_current_function_name()}] Staff Thing {staff_thing.name} wrapup failed')

        self._staff_thing_list.remove(staff_thing)
        return True

    def _store_staff_thing_info(self, target_staff_thing: MXStaffThing) -> None:
        if not os.path.exists(self.DEFAULT_STAFF_THING_STORE_PATH):
            json_file_write(self.DEFAULT_STAFF_THING_STORE_PATH, dict(data=[]), mode='w')

        if os.geteuid() == 0:
            original_user = os.environ.get('SUDO_USER')
            if not original_user:
                raise ValueError('SUDO_USER environment variable is not set. Unable to determine the original user.')

            user_info = pwd.getpwnam(original_user)
            uid = user_info.pw_uid
            gid = user_info.pw_gid

            os.chown(self.DEFAULT_STAFF_THING_STORE_PATH, uid, gid)
            os.chmod(self.DEFAULT_STAFF_THING_STORE_PATH, 0o644)

        staff_thing_info_list = []
        staff_thing_info_file: Dict[str, list] = json_file_read(self.DEFAULT_STAFF_THING_STORE_PATH)
        staff_thing_info_list = staff_thing_info_file['data']

        if not target_staff_thing.staff_dict() in staff_thing_info_list:
            staff_thing_info_list.append(target_staff_thing.staff_dict())

        json_file_write(self.DEFAULT_STAFF_THING_STORE_PATH, dict(data=staff_thing_info_list))

    def _delete_staff_thing_info(self, target_staff_thing: MXStaffThing) -> None:
        staff_thing_info_file = json_file_read(self.DEFAULT_STAFF_THING_STORE_PATH)
        staff_thing_info_list = staff_thing_info_file['data']
        staff_thing_info_list = [info for info in staff_thing_info_list if info['id'] != target_staff_thing.name and info['name'] != target_staff_thing.nick_name]
        json_file_write(self.DEFAULT_STAFF_THING_STORE_PATH, dict(data=staff_thing_info_list))

    async def _load_staff_thing_info(self) -> List[MXStaffThing]:
        staff_thing_info_list = json_file_read(self.DEFAULT_STAFF_THING_STORE_PATH)
        if not staff_thing_info_list:
            return []
        else:
            staff_thing_info_list = [self._create_staff(staff_thing_info) for staff_thing_info in staff_thing_info_list['data']]

        return staff_thing_info_list

    @override
    def _subscribe_init_topic_list(self, staff_thing: MXThing) -> None:
        topic_list = [
            MXProtocolType.Base.MT_REQUEST_REGISTER_INFO.value % staff_thing.name,
            MXProtocolType.Base.MT_RESULT_REGISTER.value % staff_thing.name,
            MXProtocolType.Base.MT_RESULT_UNREGISTER.value % staff_thing.name,
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE.value % staff_thing.name,
        ]

        for topic in topic_list:
            self._subscribe(topic)

    @override
    def _subscribe_service_topic_list(self, thing: MXThing):
        topic_list = []

        if find_class_in_hierarchy(thing, MXManagerThing) or type(thing) is MXThing:
            target_thing = self._thing_data
            for service in target_thing.function_list:
                topic_list += [
                    MXProtocolType.Base.MT_IN_EXECUTE.value % (service.name, target_thing.name),
                ]
        elif find_class_in_hierarchy(thing, MXStaffThing):
            target_thing = thing
            for function in target_thing.function_list:
                topic_list += [
                    MXProtocolType.Base.MT_EXECUTE.value % (function.name, target_thing.name, '+', '+'),
                    (MXProtocolType.Base.MT_EXECUTE.value % (function.name, target_thing.name, '', '')).rstrip('/'),
                ]
        else:
            raise ValueError(f'Unknown type instance: {type(thing)}')

        for topic in topic_list:
            self._subscribe(topic)

    def _get_staff_thing_by_name(self, name: str, staff_thing_pool: List[MXStaffThing] = None) -> MXStaffThing:
        if staff_thing_pool is None:
            staff_thing_pool = self._staff_thing_list

        for staff_thing in staff_thing_pool:
            if staff_thing.name == name:
                return staff_thing

        return False

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
    def _whole_thing_list(self) -> List[MXThing]:
        return [self, *self._staff_thing_list]
