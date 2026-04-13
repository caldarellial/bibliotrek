from app.database import SessionDep
from app.dependencies.google_books import GoogleBooksVolume
from app.models import Book, Author, BookAuthorLink
from sqlmodel import select

def get_or_create_author(author_name: str, session: SessionDep) -> Author:
  author = session.exec(select(Author).where(Author.name == author_name)).first()
  if not author:
    author = Author(name=author_name)
    session.add(author)
  return author

def sync_google_book_entries(books: list[GoogleBooksVolume], session: SessionDep):
  for book in books:
    existing_book = session.exec(select(Book).where(Book.book_id == book.id)).first()
    if existing_book:
      continue
    if not book.isbn_10() and not book.isbn_13():
      continue
    if not book.volumeInfo.title:
      continue
    new_book = Book(
      book_id=book.id,
      title=book.volumeInfo.title,
      subtitle=book.volumeInfo.subtitle if book.volumeInfo.subtitle else None,
      isbn_10=book.isbn_10() if book.isbn_10() else None,
      isbn_13=book.isbn_13() if book.isbn_13() else None,
      thumbnail_url=book.volumeInfo.imageLinks.thumbnail if book.volumeInfo.imageLinks else None,
    )
    session.add(new_book)
    authors = [get_or_create_author(author, session) for author in book.volumeInfo.authors or []]
    for author in authors:
      book_author_link = BookAuthorLink(book_id=new_book.id, author_id=author.id)
      session.add(book_author_link)
  session.commit()