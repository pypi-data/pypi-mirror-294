from big_thing_py.common import *
from big_thing_py.core.request import *
from big_thing_py.core.mqtt_message import *
from big_thing_py.core.argument import *
from big_thing_py.core.service import *
from big_thing_py.core.service_model import SkillFunction, SkillFunctionArgument
from big_thing_py.core.service_model import Objects as Skill

import asyncio


class MXFunction(MXService):

    def __init__(
        self,
        func: Callable,
        tag_list: List[MXTag],
        return_type: MXType = None,
        category: Union[SkillValue, SkillFunction] = Skill.testSkill.Functions.testSkillFunction,
        name: str = '',
        energy: float = 0,
        desc: str = '',
        thing_name: str = '',
        middleware_name: str = '',
        arg_list: List[MXArgument] = None,
        exec_time: float = 0,
        timeout: float = 0,
        range_type: MXRangeType = MXRangeType.SINGLE,
    ) -> None:
        super().__init__(
            func=func,
            tag_list=tag_list,
            name=name,
            category=category,
            energy=energy,
            desc=desc,
            thing_name=thing_name,
            middleware_name=middleware_name,
        )

        # NOTE (thsvkd): generate getter MXFunction instance of target MXValue
        if issubclass(self._category, SkillValue):
            self._return_type = self._category.value_type.type
            self._arg_list = []
        else:
            self._arg_list = arg_list
            if self._arg_list is None:
                arguments: List[SkillFunctionArgument] = self._category.arguments
                self._arg_list = [
                    MXArgument(
                        name=arg.argument_id,
                        type=arg.argument_type.type,
                        bound=arg.argument_type.bound,
                    )
                    for arg in arguments
                ]

        # TODO (thsvkd): Not supported (ENUM, LIST, DICT) MXType yet
        if not return_type is None:
            self._return_type = return_type
        elif self._category.return_type in [MXType.ENUM, MXType.LIST, MXType.DICT]:
            self._return_type = MXType.STRING
        else:
            self._return_type = self._category.return_type

        self._exec_time = exec_time
        self._timeout = timeout
        # TODO: range_type will be removed from MXFunction
        self._range_type = range_type

        self._return_value = None
        self._running = False
        self._running_scenario_list: List[str] = []

        if self._return_type in [MXType.UNDEFINED] or isinstance(self._return_type, str):
            raise MXValueError('return_type cannot be undefined or `str` type')
        if (not len(self._arg_list) == len(get_function_info(self._func)['args'])) if self._func else False:
            raise MXValueError(
                f'Length of argument list must be same with callback function.\n'
                f'given: {len(self._arg_list)}, expected: {len(get_function_info(self._func)["args"])}'
            )

        # TODO: return type detection feature
        # if not self._return_type or self._return_type in [MXType.UNDEFINED]:
        #     func_info = get_function_info(self._func)
        #     self._return_type = MXType().get(func_info[2])
        #     raise MXValueError('type must be specified')
        # elif self._return_type in [MXType.UNDEFINED]:
        #     raise MXValueError('type cannot be undefined or void')

    def __eq__(self, o: 'MXFunction') -> bool:
        instance_check = isinstance(o, MXFunction)
        arg_list_check = o._arg_list == self._arg_list
        return_type_check = o._return_type == self._return_type
        exec_time_check = o._exec_time == self._exec_time
        timeout_check = o._timeout == self._timeout
        range_type_check = o._range_type == self._range_type

        return (
            super().__eq__(o) and instance_check and arg_list_check and return_type_check and exec_time_check and timeout_check and range_type_check
        )

    def __getstate__(self):
        state = super().__getstate__()

        state['_return_type'] = self._return_type
        state['_arg_list'] = self._arg_list
        state['_exec_time'] = self._exec_time
        state['_timeout'] = self._timeout
        state['_range_type'] = self._range_type

        del state['_return_value']
        del state['_running']
        del state['_running_scenario_list']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._type = state['_type']
        self._min = state['_min']
        self._max = state['_max']
        self._cycle = state['_cycle']
        self._format = state['_format']

        self._return_value = None
        self._running = False
        self._running_scenario_list = []

    async def _async_wrapper(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    async def execute(self, execute_request: Union[MXExecuteRequest, MXInnerExecuteRequest]) -> Tuple['MXFunction', MXErrorCode]:
        execute_msg = execute_request.trigger_msg
        self._running_scenario_list.append(execute_msg.scenario)
        execute_request.timer_start()

        execute_msg = execute_request._trigger_msg
        MXLOG_DEBUG(f'[FUNC RUN] run {self._name} function by {execute_msg.scenario}', 'green')

        try:
            if not isinstance(execute_msg, MXExecuteMessage):
                raise Exception(f'[{get_current_function_name()}] Wrong ExecuteMessage type - execute_msg: {type(execute_msg)}')

            self._running = True
            execute_request.result_msg.error = MXErrorCode.NO_ERROR

            if self._timeout:
                if asyncio.iscoroutinefunction(self._func):
                    self._return_value = await asyncio.wait_for(self._func(*execute_msg.tuple_arguments()), timeout=self._timeout)
                else:
                    self._return_value = await asyncio.wait_for(self._async_wrapper(*execute_msg.tuple_arguments()), timeout=self._timeout)
            else:
                if asyncio.iscoroutinefunction(self._func):
                    self._return_value = await self._func(*execute_msg.tuple_arguments())
                else:
                    self._return_value = await self._async_wrapper(*execute_msg.tuple_arguments())
        except KeyboardInterrupt as e:
            # TODO: for wrapup main thread, but not test it yet
            print_error(e)
            MXLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except asyncio.CancelledError as e:
            # TODO: for wrapup main thread, but not test it yet
            print_error(e)
            MXLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except asyncio.TimeoutError as e:
            MXLOG_DEBUG(f'[FUNC TIMEOUT] function {self._name} by scenario {execute_msg.scenario} was timeout!!!', 'yellow')
            execute_request.result_msg.error = MXErrorCode.TIMEOUT
        except BaseException as e:
            print_error(e)
            MXLOG_DEBUG(
                f'[FUNC FAIL] function {self._name} by scenario {execute_msg.scenario} is failed while executing!!!',
                'red',
            )
            execute_request.result_msg.error = MXErrorCode.FAIL
        else:
            execute_request.result_msg.error = MXErrorCode.NO_ERROR
        finally:
            if isinstance(self._return_value, str) and is_base64(self._return_value) and self._return_type != MXType.BINARY:
                raise MXValueError('return value is base64, but type is not BINARY')

            self._running = False
            self._running_scenario_list.remove(execute_msg.scenario)

            execute_request.result_msg.return_value = self._return_value
            execute_request.timer_end()
            MXLOG_DEBUG(
                f'[FUNC END] function {self._name} end. -> return value : {self._return_value}, duration: {execute_request.duration():.4f} Sec',
                'green',
            )

            return execute_request

    def dict(self) -> dict:
        return {
            'name': self._name,
            'category': self._category.function_id if issubclass(self._category, SkillFunction) else self._category.value_id,
            'description': self._desc,
            'exec_time': self._exec_time * 1000 if self._exec_time is not None else 0,
            'return_type': self._return_type.value,
            'energy': self._energy,
            'tags': [tag.dict() for tag in self._tag_list],
            'use_arg': 1 if len(self._arg_list) > 0 else 0,
            'arguments': [argument.dict() for argument in self._arg_list] if self._arg_list else [],
        }

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_execute_result_message(
        self,
        execute_request: Union[MXExecuteRequest, MXInnerExecuteRequest],
    ) -> MXExecuteResultMessage:
        trigger_msg = execute_request.trigger_msg
        result_msg = execute_request.result_msg

        if isinstance(result_msg.return_value, BinaryBase64):
            return_value = str(result_msg.return_value)
        else:
            return_value = result_msg.return_value

        return MXExecuteResultMessage(
            function_name=trigger_msg.function_name,
            thing_name=result_msg.thing_name,
            middleware_name=result_msg.middleware_name,
            scenario=trigger_msg.scenario,
            client_id=trigger_msg.client_id,
            request_ID=trigger_msg.request_ID,
            return_type=result_msg.return_type,
            return_value=return_value,
            error=result_msg.error,
            action_type=execute_request.action_type,
        )

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
    def exec_time(self) -> float:
        return self._exec_time

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def arg_list(self) -> List[MXArgument]:
        return self._arg_list

    @property
    def return_type(self) -> MXType:
        return self._return_type

    @property
    def return_value(self) -> Union[int, float, str, bool]:
        return self._return_value

    @property
    def running(self) -> bool:
        return self._running

    @property
    def range_type(self) -> MXRangeType:
        return self._range_type

    @property
    def running_scenario_list(self) -> List[str]:
        return self._running_scenario_list

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    @exec_time.setter
    def exec_time(self, exec_time: float) -> None:
        self._exec_time = exec_time

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        self._timeout = timeout

    @arg_list.setter
    def arg_list(self, arg_list: List[MXArgument]) -> None:
        self._arg_list = arg_list

    @return_type.setter
    def return_type(self, return_type: MXType) -> None:
        self._return_type = return_type

    @return_value.setter
    def return_value(self, return_value: Union[int, float, str, bool]) -> None:
        self._return_value = return_value

    @running.setter
    def running(self, running: bool) -> None:
        self._running = running

    @range_type.setter
    def range_type(self, range_type: MXRangeType) -> None:
        self._range_type = range_type


if __name__ == '__main__':
    pass
