from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID
from app.models import Book, SessionDep

router = APIRouter()

class CreateBookOut(BaseModel):
  id: UUID
  title: str

@router.post("/books")
def create_book(book: Book, session: SessionDep) -> dict[str, CreateBookOut]:
  session.add(book)
  session.commit()
  return {"book": CreateBookOut(id=book.id, title=book.title)}