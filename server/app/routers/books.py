from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from uuid import UUID
from app.models import Author, Book, SessionDep
from app.config import get_settings
from app.dependencies.google_books import (
  GoogleBooksVolume,
  search_books,
  GoogleBooksServiceDep,
)
from app.models.public_out import BookOut
from app.tasks.sync_google_book_entries import sync_google_book_entries
from sqlmodel import select
router = APIRouter(prefix="/books")
_settings = get_settings()
class CreateBookOut(BaseModel):
  id: UUID
  title: str

@router.get("/search")
def search(query: str, service: GoogleBooksServiceDep, background_tasks: BackgroundTasks, session: SessionDep) -> dict[str, list[GoogleBooksVolume]]:
  result = search_books(query, service)
  if result.items:
    background_tasks.add_task(sync_google_book_entries, session=session, books = result.items)
  return {"books": result.items or []}

@router.get("/")
def get_books(session: SessionDep) -> dict[str, list[BookOut]]:
  books = session.exec(select(Book)).all()
  return {"books": [BookOut.from_book(book) for book in books]}

@router.post("/")
def create_book(book: Book, session: SessionDep) -> dict[str, CreateBookOut]:
  session.add(book)
  session.commit()
  return {"book": CreateBookOut(id=book.id, title=book.title)}