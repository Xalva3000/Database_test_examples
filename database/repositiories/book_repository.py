from sqlalchemy import insert, select, delete, update

from database.abstractions.abc_repository import Repository
from database.models import Book
from database.schemes.book_schemes import BookCreate, BookUpdate, BookUpdatePartial
from contextlib import contextmanager


class BookRepository(Repository):
    def __init__(self, engine, test=False):
        self.engine = engine

    @contextmanager
    def connect(self):
        with self.engine.begin() as connection:
            yield connection

    def get(self, book_id):
        stmt = select(Book).filter_by(id=book_id)
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.one_or_none()

    def get_all(self):
        stmt = select(Book).order_by(Book.id)
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.all()

    def create(self, book_in: BookCreate):
        stmt = insert(Book).values(**book_in.model_dump()).returning(Book)
        with self.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result

    def update(self, book_id: Book | int, book_update: BookUpdate | BookUpdatePartial, partial=False):
        # for k, v in book_update.model_dump(exclude_unset=partial).items():

        stmt = update(Book).where(
            Book.id == book_id
        ).values(
            **book_update.model_dump(exclude_unset=partial)
        ).returning(Book)
        with self.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.one_or_none()

    def delete(self, book_id: int):
        stmt = delete(Book).where(Book.id == book_id)
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.rowcount

    def delete_all(self):
        stmt = delete(Book)
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.rowcount



    # def select_all_id():
    #     stmt = select(Book.id).order_by(Book.id)
    #     result = session.execute(stmt)
    #     return result.scalars().all()
    #
    # def select_book(
    #     id,
    #     engine: Engine = db_connect.engine
    # ):
    #     with engine.begin() as conn:
    #         stmt = select(Book).where(id=id)
    #         result = conn.execute(stmt)
    #
    #     return result
    #

    #
    # def select_all_txt(session: Session = db_connect.session_dependency()):
    #     stmt = text("select * from book;")
    #     result = session.execute(stmt)
    #     return result.all()
    #
    # def select_by_title(title: str, session: Session = db_connect.session_dependency()):
    #     stmt = select(Book).filter(Book.title == title)
    #     result = session.execute(stmt)
    #     return result.scalars().all()
    #
    # def select_title_contains(title: str, session: Session = db_connect.session_dependency()):
    #     # stmt = select(Book).filter(Book.title.ilike(f'%{title}%')).all()
    #     stmt = select(Book).where(Book.title.contains(title))
    #     result = session.execute(stmt)
    #     return result.scalars().all()
    #
    #
    # def get_statement():
    #     stmt = insert(Book).values(title='Преступление и наказание', author='Достоевский ФМ')
    #     return stmt.compile(stmt, dialect=postgresql.dialect())

# if __name__ == "__main__":
#     repo = BookRepository(db_connect=db_connect)
#     repo.get(1)