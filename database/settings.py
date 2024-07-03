from environs import Env
from os import name as os_name


class DBSettings:
    def __init__(self, path: str):
        env = Env()
        env.read_env(path)
        self.DB_NETLOC = env('DB_NETLOC')
        self.DB_PORT = env('DB_PORT')
        self.DB_USER = env('DB_USER')
        self.DB_PASS = env('DB_PASS')
        self.DB_NAME = env('DB_NAME')

    def load_driver_url(self, *, dbs: str = "postgresql", driver: str = "asyncpg") -> str:

        url = f'{dbs}{"+" + driver if driver else ""}://{self.DB_USER}:{self.DB_PASS}@' \
              f'{self.DB_NETLOC}:{self.DB_PORT}/{self.DB_NAME}'
        return url


if os_name == 'nt':
    env_path = r".\.keys\.env"
    env_path_test = r".\.keys\.env_test_db"
else:
    raise ValueError('Unknown OS data. No path to .env file.')


settings = DBSettings(env_path)


