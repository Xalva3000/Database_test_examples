import logging
from random import randint

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from database.connect import db_connect
from sqlalchemy import text, insert, select, and_, or_, desc, update, bindparam, delete, inspect, Engine

from database.models import Book, Story, Page
from database.db_utils import log_decor, timer, fake, fake_eng


logger = logging.getLogger(__name__)


def get_hello(session: Session = db_connect.session_dependency()):
    stmt = text("select 'hello world';")
    result = session.execute(stmt)
    return result.all()


class BookQuery:
    @staticmethod
    def insert_book(
        author: str,
        title: str,
        session: Session = db_connect.session_dependency()
    ):
        stmt = insert(Book).values(author=author, title=title)
        result = session.execute(stmt)
        session.commit()
        return result

    @timer
    @staticmethod
    def select_all_id(session: Session = db_connect.session_dependency()):
        stmt = select(Book.id).order_by(Book.id)
        result = session.execute(stmt)
        return result.scalars().all()

    @timer
    @staticmethod
    def select_book(
        id,
        engine: Engine = db_connect.engine
    ):
        with engine.begin() as conn:
            stmt = select(Book).where(id=id)
            result = conn.execute(stmt)

        return result

    @timer
    @staticmethod
    def update_book(
        id,
        values: dict,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = update(Book).where(id=id).values(**values)
            result = conn.execute(stmt)
        return result.rowcount

    @timer
    @staticmethod
    def delete_book(
        id,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = delete(Book).where(id=id)
            result = conn.execute(stmt)
        return result.rowcount

    @staticmethod
    def select_all_txt(session: Session = db_connect.session_dependency()):
        stmt = text("select * from book;")
        result = session.execute(stmt)
        return result.all()


    @staticmethod
    def select_by_title(title: str, session: Session = db_connect.session_dependency()):
        stmt = select(Book).filter(Book.title == title)
        result = session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def select_title_contains(title: str, session: Session = db_connect.session_dependency()):
        # stmt = select(Book).filter(Book.title.ilike(f'%{title}%')).all()
        stmt = select(Book).where(Book.title.contains(title))
        result = session.execute(stmt)
        return result.scalars().all()

    @timer
    @log_decor
    @staticmethod
    def get_statement():
        stmt = insert(Book).values(title='Преступление и наказание', author='Достоевский ФМ')
        return stmt.compile(stmt, dialect=postgresql.dialect())


class StoryQuery:
    required_fields = 'title', 'book_id'
    secondary_fields = 'book', 'pages'

    @timer
    @staticmethod
    def insert_story(
        title,
        book_id,
        session: Session = db_connect.session_dependency()
    ):

        stmt = insert(Story).values(title=title, book_id=book_id)
        result = session.execute(stmt)
        session.commit()
        return result

    @timer
    @staticmethod
    def select_all_id(session: Session = db_connect.session_dependency()):
        stmt = select(Story.id).order_by(Story.id)
        result = session.execute(stmt)
        return result.scalars().all()

    @timer
    @staticmethod
    def select_story(
        id,
        engine: Engine = db_connect.engine
    ):
        with engine.begin() as conn:
            stmt = select(Story).where(id=id)
            result = conn.execute(stmt)

        return result

    @timer
    @staticmethod
    def update_story(
        id,
        values: dict,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = update(Story).where(id=id).values(**values)
            result = conn.execute(stmt)
        return result.rowcount

    @timer
    @staticmethod
    def delete_story(
        id,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = delete(Story).where(id=id)
            result = conn.execute(stmt)
        return result.rowcount


class PageQuery:
    required_fields = 'page_text', 'story_id'
    secondary_fields = 'story'

    @timer
    @staticmethod
    def insert_page(
        page_text,
        story_id,
        session: Session = db_connect.session_dependency()
    ):
        stmt = insert(Page).values(page_text=page_text, story_id=story_id)
        result = session.execute(stmt)
        session.commit()
        return result

    @timer
    @staticmethod
    def select_page(
        id,
        engine: Engine = db_connect.engine
    ):
        with engine.begin() as conn:
            stmt = select(Page).where(id=id)
            result = conn.execute(stmt)

        return result

    @timer
    @log_decor
    @staticmethod
    def update_page(
        id,
        values: dict,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = update(Page).where(id=id).values(**values)
            result = conn.execute(stmt)
        return result.rowcount

    @timer
    @log_decor
    @staticmethod
    def delete_page(
        id,
        engine: Engine = db_connect.engine,
    ):
        with engine.begin() as conn:
            stmt = delete(Page).where(id=id)
            result = conn.execute(stmt)
        return result.rowcount


class LearningQuery:

    @staticmethod
    def query_1(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = text('select * from book;')
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_2(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(Book).where(
                and_(Book.title.startswith("Rea"),
                     Book.author.contains("Lov"))
            )
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_3(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(Book).where(
                and_(Book.title.startswith("Rea"),
                     Book.author.contains("Lov"))
            )
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_4(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(Book).where(
                or_(Book.title.startswith("Rea"),
                     Book.author.contains("Lov"))
            )
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_5(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(Book.title, Book.author).where(
                or_(
                    Book.title.startswith("Rea"),
                    Book.author.contains("Lov")
                )
            ).order_by(
                "author"
            )
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_6(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(Book.title, Book.author).where(
                Book.id.in_([10,11])
            ).order_by(
                Book.id.desc()
            )
            result = conn.execute(stmt)
        return result.all()

    @staticmethod
    def query_7(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = select(
                Book.id,
                (Book.title + ' ' + Book.author).label('book')
            ).where(
                Book.id.in_([10, 11])
            ).order_by(
                desc(Book.id)
            )
            result = conn.execute(stmt)
        return result.mappings().all()

    @staticmethod
    def query_8(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = insert(Book)
            values = [
                {'title': fake.catch_phrase(), 'author': fake.name()} for _ in range(3)
            ]
            result = conn.execute(stmt, values, )
        return result.rowcount

    @staticmethod
    def query_9(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = update(Book).where(
                Book.id == randint(1, 30)
            ).values(title=fake_eng.catch_phrase(), author=fake_eng.name())
            result = conn.execute(stmt)
        return result.rowcount

    @staticmethod
    def query_10(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = update(Book).where(
                Book.author == bindparam('param1')
            ).values(title=bindparam('param2'))
            values = [
                {'param1': fake.name(),'param2': fake.catch_phrase(),}
            ]
            result = conn.execute(stmt, values)
        return result.rowcount

    @staticmethod
    def query_11(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = delete(Book).where(Book.author.contains('Lov'))
            result = conn.execute(stmt)
        return result.rowcount

    @staticmethod
    def query_12(engine=db_connect.engine):
        with engine.begin() as conn:
            stmt = delete(Book).where(Book.author.contains('Lov')).returning(Book.id)
            result = conn.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def query_13(session: Session = db_connect.session_dependency()):
        book = Book(author=fake.name(), title=fake.catch_phrase())
        print("transient", inspect(book).transient)
        session.add(book)
        print("pending", inspect(book).pending)
        session.flush()
        print("persistent", inspect(book).persistent)
        session.delete(book)
        print("deleted", inspect(book).deleted)
        session.flush()
        print("deleted", inspect(book).deleted)
        # session.rollback()

        book2 = Book(author=fake.name(), title=fake.catch_phrase())
        session.add(book2)
        session.commit()
        session.close()
        print("detached", inspect(book2).detached)
