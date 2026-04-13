from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from app.models import Book, SessionDep, User, UserBookLink, select
from app.dependencies.authentication import get_current_user
from app.models.public_out import BookOut

router = APIRouter(prefix="/users/me", tags=["me"])

@router.get("/collected-books")
def get_collected_book(user: Annotated[User, Depends(get_current_user)]) -> dict[str, list[BookOut]]:
  return {"books": [BookOut.from_book(link.book) for link in user.collected_books]}

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