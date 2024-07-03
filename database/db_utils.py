from functools import wraps
from time import perf_counter
import logging
from datetime import date
from faker import Faker


fake = Faker('ru_RU')
fake_eng = Faker('en')
# fake.seed_instance(1)


logger = logging.getLogger(__name__)
# file_handler = logging.FileHandler(fr'.\logs\{date.today()}-db_logs.txt', encoding='utf-8')
# file_handler.setLevel(level=logging.INFO)

std_handler = logging.StreamHandler()
std_handler.setLevel(level=logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s',
                    handlers=[std_handler])

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__}:{(perf_counter() - start).__round__(2)}")
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