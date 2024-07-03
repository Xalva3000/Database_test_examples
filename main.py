import logging
import unittest
from datetime import date
from sys import argv

from http_libs.custom_requests import internet
from database.db_utils import fake
from database.queries import LearningQuery
from tests.test_db import launch_test_db
from tests.test_request import launch_test_request

logger = logging.getLogger(__name__)


file_handler = logging.FileHandler(fr'logs\{date.today()}-logs.txt', encoding='utf-8')
file_handler.setLevel(level=logging.DEBUG)

std_handler = logging.StreamHandler()
std_handler.setLevel(level=logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    handlers=[file_handler, std_handler])


def main():
    for func_name, query in LearningQuery.__dict__.items():
        if func_name.startswith('query'):
            print(query())


def launch_tests(name='alex', password='12345'):
    internet(name, password)
    launch_test_request()



if __name__ == "__main__":
    # if len(argv) > 1:
    #     file, mode, *args = argv
    #     print(file, mode, *args)

    main()
