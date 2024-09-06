from big_thing_py.utils.exception_util import *
from big_thing_py.utils.log_util import *
from big_thing_py.utils.json_util import *

from gmqtt import Message as MQTTMessage


def encode_MQTT_message(topic: str, payload: Union[str, dict]) -> MQTTMessage:
    try:
        if isinstance(payload, str):
            payload = bytes(payload, encoding='utf-8')
        elif isinstance(payload, dict):
            payload = dict_to_json_string(payload)

        return MQTTMessage(topic, payload)
    except Exception as e:
        print_error(e)
        raise e


def decode_MQTT_message(msg: MQTTMessage, mode=dict) -> Tuple[str, dict]:
    topic = msg.topic
    payload = msg.payload

    if isinstance(topic, bytes):
        topic = topic.decode()
    if isinstance(payload, bytes):
        payload = payload.decode()

    if isinstance(payload, str):
        if mode == str:
            return topic, payload
        elif mode == dict:
            return topic, json_string_to_dict(payload)
        else:
            raise MXNotSupportedError(f'Unexpected mode!!! - {mode}')
    elif isinstance(payload, dict):
        if mode == str:
            return topic, dict_to_json_string(payload)
        elif mode == dict:
            return topic, payload
        else:
            raise MXNotSupportedError(f'Unexpected mode!!! - {mode}')
    else:
        raise MXNotSupportedError(f'Unexpected type!!! - {type(payload)}')


def topic_split(topic: str):
    return topic.split('/')


def topic_join(topic: List[str]):
    return '/'.join(topic)


def unpack_mqtt_message(msg: MQTTMessage) -> Tuple[List[str], str]:
    topic, payload = decode_MQTT_message(msg, dict)
    topic = topic_split(topic)

    return topic, payload


def pack_mqtt_message(topic_list: List[str], payload: str) -> MQTTMessage:
    topic = topic_join(topic_list)
    msg = encode_MQTT_message(topic, payload)

    return msg
