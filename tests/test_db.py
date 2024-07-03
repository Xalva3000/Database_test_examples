from datetime import datetime
import unittest

from unittest.mock import patch, MagicMock
from database.queries import BookQuery, StoryQuery, PageQuery

from database.models import metadata

from database.settings import DBSettings, env_path_test
from database.connect import SyncDBConnect


driver_url = DBSettings(env_path_test).load_driver_url(driver='psycopg2')
print(env_path_test)
test_db_connect = SyncDBConnect(driver_url=driver_url, echo=True)
# metadata.bind = test_db_connect.engine


class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_engine = self.mock_session = MagicMock()
        self.test_engine = test_db_connect.engine
        # print(test_db_connect.engine)
        # metadata.create_all(test_db_connect.engine)

    @patch('database.connect.db_connect.session_dependency')
    def test_select_all(self, mock_session):
        test_created_at = datetime.utcnow()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.all.return_value = [(1, 'test_title', 'test_text', test_created_at)]

        result = BookQuery.select_all_txt(mock_session)
        print(result)
        self.assertEqual(result[0], (1, 'test_title', 'test_text', test_created_at))

    def test_select_all_text(self):
        result = BookQuery.select_all_id(test_db_connect.session_dependency())
        print(result)


    def tearDown(self) -> None:
        # metadata.drop_all(test_db_connect.engine)
        pass

def launch_test_db():
    unittest.main(r"tests\test_db")


if __name__ == "__main__":
    launch_test_db()
