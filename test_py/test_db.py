import pytest
from _decimal import Decimal

from database.connect import SyncDBConnect
from database.models import metadata, Book

from database.settings import DBSettings, env_path
from database.repositiories.book_repository import BookRepository
from database.schemes.book_schemes import BookUpdate, BookCreate, BookUpdatePartial
from database.db_utils import fake
from pydantic import ValidationError


driver_url = DBSettings(env_path, test=True).load_driver_url(driver='psycopg2')

test_db_connect = SyncDBConnect(driver_url=driver_url, echo=False)
metadata.bind = test_db_connect.engine


class TestBookRepository:
    def setup_method(self):
        metadata.create_all(test_db_connect.engine)
        self.library = BookRepository(test_db_connect.engine)
        for _ in range(10):
            new_book = BookCreate(author=fake.name(), title=fake.catch_phrase())
            self.library.create(new_book)

    @pytest.mark.tryfirst
    def test_get_existing(self):
        result = self.library.get(1)
        assert type(result), tuple

    def test_get_not_existing(self):
        result = self.library.get(11)
        assert result is None

    def test_get_all(self):
        result = self.library.get_all()
        assert len(result), 10

    def test_get_all_ordering(self):
        result = self.library.get_all()
        assert result, sorted(result, key=lambda tpl: tpl[0])



    def test_delete(self):
        result = self.library.delete(1)
        assert result == 1
        assert self.library.get(1) is None


    @pytest.mark.trylast
    def test_delete_all(self):
        result = self.library.delete_all()
        assert result == 10
        assert self.library.get(1) is None
        assert len(self.library.get_all()) == 0

    def test_update_existing(self):
        book = self.library.get(1)
        author = 'Lovecraft HP'
        title = 'Reanimator'
        book_in = BookUpdate(author=author, title=title)
        result = self.library.update(book.id, book_in)
        new_book_q = self.library.get(1)
        assert result == new_book_q
        assert new_book_q.id == 1
        assert new_book_q.author == author
        assert new_book_q.title == title


    @pytest.mark.parametrize(
        'title, author, expected',
    [
        ('Lovecraft HP', 'Reanimator', 1),
        pytest.param(1, 42, 1, marks=pytest.mark.xfail),
        pytest.param(1.2, 42.2, 1, marks=pytest.mark.xfail),
        pytest.param(Decimal('2.3'), Decimal('2.3'), 1, marks=pytest.mark.xfail),
        pytest.param(True, False, 1, marks=pytest.mark.xfail),
        ('1', '2', 1)
    ])
    def test_update_existing_parametrized(self, title, author, expected):
        book_in = BookUpdate(author=author, title=title)
        result = self.library.update(1, book_in)
        new_book_q = self.library.get(1)
        assert new_book_q.id == expected
        assert result == new_book_q
        assert new_book_q.author == author
        assert new_book_q.title == title

    def test_update_non_existing(self):
        author = 'Lovecraft HP'
        title = 'Reanimator'
        book_in = BookUpdate(author=author, title=title)
        result = self.library.update(11, book_in)
        new_book = self.library.get(11)
        assert result is None
        assert new_book is None


    def test_update_partial(self):
        pass

    def test_create(self):
        pass

    @pytest.mark.skip
    def test_for_skip(self):
        pass



    def teardown_method(self):
        metadata.drop_all(test_db_connect.engine)
