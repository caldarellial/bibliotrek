from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Any, List, Optional, cast
from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, delete, select, func, Relationship, text, UniqueConstraint

from app.database import SessionDep

class BaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    _ts = cast(Any, DateTime(timezone=True))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=_ts,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "nullable": False,
        },
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=_ts,
        sa_column_kwargs={"onupdate": func.now(), "nullable": True},
    )
       

class User(BaseTable, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    password: str
    collected_books: List["UserBookLink"] = Relationship(back_populates="user")

class Book(BaseTable, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    book_id: str
    title: str
    subtitle: Optional[str] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    thumbnail_url: Optional[str] = None
    authors: List["BookAuthorLink"] = Relationship(back_populates="book")
    collected_by_users: List["UserBookLink"] = Relationship(back_populates="book")

class Author(BaseTable, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    books: List["BookAuthorLink"] = Relationship(back_populates="author")

class UserBookLink(BaseTable, table=True):    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    book_id: UUID = Field(foreign_key="book.id")
    user: User = Relationship(back_populates="collected_books")
    book: Book = Relationship(back_populates="collected_by_users")

class BookAuthorLink(BaseTable, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    book_id: UUID = Field(foreign_key="book.id")
    author_id: UUID = Field(foreign_key="author.id")
    book: Book = Relationship(back_populates="authors")
    author: Author = Relationship(back_populates="books")

__all__ = ["User", "SessionDep", "select", "delete", "UserBookLink", "Book", "Author", "BookAuthorLink"]
    