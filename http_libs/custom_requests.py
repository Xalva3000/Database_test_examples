from datetime import date
from functools import wraps
from pprint import pprint
from time import perf_counter

import requests
import logging


logger = logging.getLogger(__name__)

# file_handler = logging.FileHandler(filename=f"logs\{date.today()}-request-logging.txt", encoding='utf-8')
# file_handler.setLevel(logging.INFO)

std_handler = logging.StreamHandler()
std_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[std_handler])

# path = 'https://google.com'
# path = "https://httpbin.org"
path = 'http://storage-monitor.ru'

# response = requests.get(path)
#
# pprint(response.ok)
# pprint(response.text)
# pprint(response.headers)
# pprint(response.request.headers)

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        logger.info(f"{(perf_counter() - start).__round__(2)}")
        return result
    return wrapper

def log_decor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Запуск {func.__name__}...')
        result = func(*args, **kwargs)
        logger.info(f'Succeed {func.__name__}. Передается значение...')
        return result
    return wrapper


class CustomResponse:
    def __init__(self, path):
        self.path = path
        self.response = self.get_response()

    @timer
    @log_decor
    def get_response(self):
        response = requests.get(self.path, timeout=3)
        return response

    @timer
    @log_decor
    def get_response_headers(self):
        return self.response.headers

    @timer
    @log_decor
    def get_response_status(self):
        return self.response.status_code

    @timer
    @log_decor
    def get_cookies(self):
        return self.response.cookies


    @timer
    @log_decor
    def get_authentication(self, username, password):
        login_path = f"{self.path}/basic-auth/{username}/{password}"
        response = requests.get(login_path, auth=(username, password))
        return response


def internet(username, password):
    path = "https://httpbin.org"


    response = CustomResponse(path)

    status = response.get_response_status()
    print(status)
    headers = response.get_response_headers()
    for key, value in headers.items():
        print(key, ':', value)

    print(response.get_cookies())

    auth = response.get_authentication(username, password)
    print(auth.text)



if __name__ == "__main__":
    internet('alex', '12345')
