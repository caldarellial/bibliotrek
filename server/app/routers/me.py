from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlmodel import func, col
from app.models import Book, SessionDep, User, UserBookLink, select
from app.dependencies.authentication import get_current_user
from app.models.public_out import BookOut

router = APIRouter(prefix="/users/me", tags=["me"])

class GetCollectedBooksResponse(BaseModel):
  books: list[BookOut]
  total: int

@router.get("/collected-books")
def get_collected_book(user: Annotated[User, Depends(get_current_user)], session: SessionDep, page: int = 0, page_size: int = 10) -> GetCollectedBooksResponse:
  paginated_books_statement = select(Book).join(UserBookLink).where(UserBookLink.user_id == user.id).offset(page * page_size).limit(page_size)
  paginated_books = session.exec(paginated_books_statement).all()
  total_books = session.exec(select(func.count(col(Book.id))).join(UserBookLink).where(UserBookLink.user_id == user.id)).first() or 0
  return GetCollectedBooksResponse(books=[BookOut.from_book(book) for book in paginated_books], total=total_books)

class AddCollectedBookRequest(BaseModel):
  book_id: UUID

@router.post("/collected-books")
def add_collected_book(addCollectedBookRequest: AddCollectedBookRequest, user: Annotated[User, Depends(get_current_user)], session: SessionDep) -> dict[str, str]:
  book = session.exec(select(Book).where(Book.id == addCollectedBookRequest.book_id)).first()
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  user.collected_books.append(UserBookLink(book_id=book.id, user_id=user.id))
  session.add(user)
  session.commit()
  return {"message": "Book added to collected books"}