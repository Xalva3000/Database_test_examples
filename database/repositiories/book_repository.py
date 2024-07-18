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


    def select_by_title(self, title: str):
        stmt = select(Book).filter(Book.title == title)
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.scalars().all()

    def select_title_contains(self, title: str):
        stmt = select(Book).where(Book.title.contains(title))
        with self.connect() as conn:
            result = conn.execute(stmt)
        return result.scalars().all()



# if __name__ == "__main__":
#     repo = BookRepository(db_connect=db_connect)
#     repo.get(1)
