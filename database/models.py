from sqlalchemy import func, text as text_func, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

Base = declarative_base()

metadata = Base.metadata


# class AbstractModel(Base):
#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


#     @classmethod
#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()
# @as_declarative()

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    author: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    stories: Mapped[list["Story"]] = relationship(back_populates="book", uselist=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(),
                        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(),
                        server_default=text_func("TIMEZONE('utc', now())"),
                        onupdate=func.now(),
                        server_onupdate=func.now())

    def __str__(self):
        return f"Book<{self.id}{self.title[:5]}...>"


class Story(Base):
    __tablename__ = 'story'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"))
    book: Mapped["Book"] = relationship("Book", back_populates="stories")

    pages: Mapped[list["Page"]] = relationship(back_populates="story", uselist=True)


class Page(Base):
    __tablename__ = 'page'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    page_text: Mapped[str] = mapped_column(nullable=False)

    story_id: Mapped[int] = mapped_column(ForeignKey("story.id", ondelete="CASCADE"))
    story: Mapped["Story"] = relationship("Story", back_populates="pages")



