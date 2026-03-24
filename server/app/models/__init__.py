from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, delete, select, Column, TIMESTAMP, func, Relationship, text

from app.database import SessionDep

class BaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "nullable": True}
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
    author_id: UUID = Field(foreign_key="author.id")
    author: "Author" = Relationship(back_populates="books")
    collected_by_users: List["UserBookLink"] = Relationship(back_populates="book")

class Author(BaseTable, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    books: List["Book"] = Relationship(back_populates="author")

class UserBookLink(BaseTable, table=True):    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    book_id: UUID = Field(foreign_key="book.id")
    user: User = Relationship(back_populates="collected_books")
    book: Book = Relationship(back_populates="collected_by_users")

__all__ = ["User", "SessionDep", "select", "delete", "UserBookLink", "Book", "Author"]
    