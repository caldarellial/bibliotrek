from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.models import Author, Book


class BookOut(BaseModel):
  id: UUID
  title: str
  subtitle: Optional[str] = None
  isbn_10: Optional[str] = None
  isbn_13: Optional[str] = None
  thumbnail_url: Optional[str] = None
  authors: List[Author]

  @classmethod
  def from_book(cls, book: Book) -> "BookOut":
    return cls(id=book.id, title=book.title, subtitle=book.subtitle, isbn_10=book.isbn_10, isbn_13=book.isbn_13, thumbnail_url=book.thumbnail_url, authors=[author.author for author in book.authors])