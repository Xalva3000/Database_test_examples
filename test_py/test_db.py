import pytest
from _decimal import Decimal
from sqlalchemy import text

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
        for _ in range(9):
            new_book = BookCreate(author=fake.name(), title=fake.catch_phrase())
            self.library.create(new_book)
        self.library.create(BookCreate(author="Пушкин АС", title="Избранное"))

    def teardown_method(self):
        metadata.drop_all(test_db_connect.engine)

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
        author = 'Lovecraft HP'
        title = 'Reanimator'
        book_in = BookUpdatePartial(author=author)
        result = self.library.update(10, book_in, partial=True)
        assert result.author == author
        assert result.title != title

    @pytest.mark.parametrize(
        "author, title",
        [
            ('Lovecraft HP', 'Reanimator'),
            pytest.param(1, 2, marks=pytest.mark.xfail),
            pytest.param(1.2, 42.2, marks=pytest.mark.xfail),
            pytest.param(Decimal('2.3'), Decimal('2.3'), marks=pytest.mark.xfail),
            pytest.param(True, False, marks=pytest.mark.xfail),
        ]
    )
    def test_create(self, author, title):
        book_in = BookCreate(author=author, title=title)
        result = self.library.create(book_in=book_in)
        assert result
        new_book = self.library.get(11)
        assert new_book.author == author
        assert new_book.title == title

    def test_select_by_title_existing(self):
        result = self.library.select_by_title("Избранное")
        assert result[0].title == "Избранное"

    def test_select_by_title_not_existing(self):
        result = self.library.select_by_title("123")
        assert len(result) == 0


    def test_select_by_title_contains_existing(self):
        result = self.library.select_title_contains("Изб")
        assert result[0].title == "Избранное"

    def test_select_by_author_existing(self):
        result = self.library.select_by_author("Пушкин АС")
        assert result[0].author == "Пушкин АС"

    def test_select_by_author_not_existing(self):
        result = self.library.select_by_author("123")
        assert len(result) == 0

    @pytest.mark.trylast
    def test_select_by_author_contains_existing(self):
        result = self.library.select_author_contains("Пуш")
        assert result[0].author == "Пушкин АС"

    def test_select_by_date_create(self):
        print(self.library.get(1))

    def test_timezone(self):
        #text("SET timezone = 'America/New_York'")
        with test_db_connect.engine.begin() as conn:
            result = conn.execute(text("show timezone;"))
        print(result.fetchall())

    @pytest.mark.skip
    def test_for_skip(self):
        pass


