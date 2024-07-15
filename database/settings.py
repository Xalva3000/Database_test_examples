from environs import Env
from os import name as os_name


class DBSettings:
    def __init__(self, path: str, test=False):
        env = Env()
        env.read_env(path)
        self.DB_NETLOC = env('DB_NETLOC' if not test else 'TEST_DB_NETLOC')
        self.DB_PORT = env('DB_PORT' if not test else 'TEST_DB_PORT')
        self.DB_USER = env('DB_USER' if not test else 'TEST_DB_USER')
        self.DB_PASS = env('DB_PASS' if not test else 'TEST_DB_PASS')
        self.DB_NAME = env('DB_NAME' if not test else 'TEST_DB_NAME')

    def load_driver_url(self, *, dbs: str = "postgresql", driver: str = "asyncpg") -> str:

        url = f'{dbs}{"+" + driver if driver else ""}://{self.DB_USER}:{self.DB_PASS}@' \
              f'{self.DB_NETLOC}:{self.DB_PORT}/{self.DB_NAME}'
        return url



if os_name == 'nt':
    env_path = r".\.keys\.env"
    env_path_test = r".\.keys\.test.env"
else:
    raise ValueError('Unknown OS data. No path to .env file.')


settings = DBSettings(env_path)




