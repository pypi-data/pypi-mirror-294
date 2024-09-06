from big_thing_py.common import *
from big_thing_py.utils.log_util import *
from big_thing_py.utils.exception_util import *

import json


def json_string_to_dict(json_string: str) -> Union[str, dict, list]:
    try:
        if type(json_string) not in [str, bytes]:
            raise json.JSONDecodeError('input string must be str, bytes type.', json_string, 0)
        else:
            return json.loads(json_string)

    except json.JSONDecodeError as e:
        MXLOG_DEBUG(f'[json_string_to_dict] input string must be json format string. return raw object... ', 'red')
        print_error(e)
        return json_string


def dict_to_json_string(dict_object: Union[dict, list, str], ensure_ascii: bool = True, pretty: bool = True, indent: int = 4) -> Union[str, bool]:
    try:
        if type(dict_object) == dict:
            if pretty:
                return json.dumps(dict_object, ensure_ascii=ensure_ascii, sort_keys=True, indent=indent)
            else:
                return json.dumps(dict_object, ensure_ascii=ensure_ascii)
        elif type(dict_object) == list:
            if pretty:
                return '\n'.join([json.dumps(item, ensure_ascii=ensure_ascii, sort_keys=True, indent=indent) for item in dict_object])
            else:
                return '\n'.join([json.dumps(item, ensure_ascii=ensure_ascii) for item in dict_object])
        else:
            if pretty:
                json.dumps(json.loads(dict_object), ensure_ascii=ensure_ascii, sort_keys=True, indent=indent)
            else:
                return str(dict_object)
    except Exception as e:
        MXLOG_DEBUG(f'[dict_to_json_string] input object must be dict or list or str. return False... ', 'red')
        print_error(e)
        return False
