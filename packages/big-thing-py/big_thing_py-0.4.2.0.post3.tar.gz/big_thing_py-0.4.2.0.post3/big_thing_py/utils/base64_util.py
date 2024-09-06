import base64
import re


def file_to_base64(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def base64_to_file(base64_string: str, file_path: str) -> None:
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(base64_string))


def string_to_base64(string: str) -> str:
    return base64.b64encode(string.encode()).decode()


def base64_to_string(base64_string: str) -> str:
    return base64.b64decode(base64_string).decode()


def is_base64(base64_str: str) -> bool:
    '''
    NOTE: The minimum length set to 24 characters is chosen based on common use cases,
          such as encoded hashes or small files, which typically result in a Base64
          string longer than 24 characters. This length helps reduce the chance of
          mistaking regular short strings for Base64 encoded data.
    '''
    if len(base64_str) < 24 or len(base64_str) % 4 != 0:
        return False

    pattern = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$')
    if bool(pattern.match(base64_str)):
        try:
            base64.b64decode(base64_str, validate=True)
            return True
        except Exception:
            return False
    else:
        return False


if __name__ == '__main__':
    print(is_base64('This is test string.'))
