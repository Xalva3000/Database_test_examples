from datetime import datetime
import unittest

from unittest.mock import patch, MagicMock
from database.queries import BookQuery, StoryQuery, PageQuery

from database.models import metadata

from database.settings import DBSettings, env_path
from database.connect import SyncDBConnect


driver_url = DBSettings(env_path, test=True).load_driver_url(driver='psycopg2')

test_db_connect = SyncDBConnect(driver_url=driver_url, echo=False)
metadata.bind = test_db_connect.engine


class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_engine = self.mock_session = MagicMock()
        self.test_engine = test_db_connect.engine
        # metadata.create_all(self.test_engine)

    @patch('database.connect.db_connect.session_dependency')
    def test_select_all(self, mock_session):
        test_created_at = datetime.utcnow()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.all.return_value = [(1, 'test_title', 'test_text', test_created_at)]

        result = BookQuery.select_all_txt(mock_session)

        self.assertEqual(result[0], (1, 'test_title', 'test_text', test_created_at))

    @patch('database.connect.db_connect.session_dependency')
    def test_select_all_text(self, mock_session):
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalars.return_value = MagicMock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = [(1,), (2,), (3,), (4,)]
        result = BookQuery.select_all_id(mock_session)
        self.assertEqual(len(result), 4)


    def tearDown(self) -> None:
        # metadata.drop_all(self.test_engine)
        pass
