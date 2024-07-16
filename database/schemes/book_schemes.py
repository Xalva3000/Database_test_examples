from pydantic import BaseModel


class BookBase(BaseModel):
    author: str
    title: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookUpdatePartial(BookBase):
    author: str | None = None
    title: str | None = None


class Book(BookBase):
    id: int
