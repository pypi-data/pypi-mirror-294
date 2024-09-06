from big_thing_py.common.mxtype import *
from big_thing_py.core.mqtt_message import *


class MXRequest(metaclass=ABCMeta):
    def __init__(self, trigger_msg: MXMQTTMessage = None, result_msg: MXMQTTMessage = None) -> None:
        self._action_type: MXActionType = None
        self._trigger_msg = trigger_msg
        self._result_msg = result_msg

        # seconds
        self._duration: float = 0

    def duration(self):
        return self._duration

    def timer_start(self):
        self._trigger_msg.set_timestamp(get_current_datetime())

    def timer_end(self):
        try:
            self._result_msg.set_timestamp(get_current_datetime())
            self._duration = self._result_msg.timestamp - self._trigger_msg.timestamp
        except Exception:
            self._duration = time.time() - self._trigger_msg.timestamp
        return self.duration()

    @property
    def result_msg(self):
        return self._result_msg

    @result_msg.setter
    def result_msg(self, result: MXMQTTReceiveMessage):
        self._result_msg = result

    @property
    def trigger_msg(self):
        return self._trigger_msg

    @trigger_msg.setter
    def trigger_msg(self, result: MXMQTTSendMessage):
        self._trigger_msg = result

    @property
    def action_type(self):
        return self._action_type


class MXRegisterRequest(MXRequest):
    def __init__(self, trigger_msg: MXMQTTMessage = None, result_msg: MXMQTTMessage = None) -> None:
        super().__init__(trigger_msg=trigger_msg, result_msg=result_msg)
        self._action_type = MXActionType.REGISTER

        self._trigger_msg: MXExecuteMessage
        self._result_msg: MXExecuteResultMessage


class MXExecuteRequest(MXRequest):
    def __init__(self, trigger_msg: MXExecuteMessage = None, result_msg: MXExecuteResultMessage = None) -> None:
        super().__init__(trigger_msg=trigger_msg, result_msg=result_msg)
        self._action_type = MXActionType.EXECUTE

        self._trigger_msg: MXExecuteMessage
        self._result_msg: MXExecuteResultMessage

    @property
    def result_msg(self):
        return self._result_msg

    @result_msg.setter
    def result_msg(self, result: MXExecuteResultMessage):
        self._result_msg = result

    @property
    def trigger_msg(self):
        return self._trigger_msg

    @trigger_msg.setter
    def trigger_msg(self, result: MXExecuteMessage):
        self._trigger_msg = result


class MXInnerExecuteRequest(MXRequest):
    def __init__(self, trigger_msg: MXExecuteMessage = None, result_msg: MXExecuteResultMessage = None) -> None:
        super().__init__(trigger_msg=trigger_msg, result_msg=result_msg)
        self._action_type = MXActionType.INNER_EXECUTE

        self._trigger_msg: MXExecuteMessage
        self._result_msg: MXExecuteResultMessage

    @property
    def result_msg(self):
        return self._result_msg

    @result_msg.setter
    def result_msg(self, result: MXExecuteResultMessage):
        self._result_msg = result

    @property
    def trigger_msg(self):
        return self._trigger_msg

    @trigger_msg.setter
    def trigger_msg(self, result: MXExecuteMessage):
        self._trigger_msg = result
