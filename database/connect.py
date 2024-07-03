from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.settings import settings


class SyncDBConnect:
    def __init__(self, driver_url, echo=False):
        self.engine = create_engine(driver_url, echo=echo)
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = scoped_session(
            session_factory=self.session_factory
        )
        return session

    def session_dependency(self):
        session = self.get_scoped_session()
        with session() as sess:
            return sess


url = settings.load_driver_url(driver='psycopg2')


db_connect = SyncDBConnect(
    driver_url=url,
    echo=False
)

