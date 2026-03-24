from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID
from app.models import Author, SessionDep

router = APIRouter()

class CreateAuthorOut(BaseModel):
  id: UUID
  first_name: str
  last_name: str

@router.post("/authors")
def create_author(author: Author, session: SessionDep) -> dict[str, CreateAuthorOut]:
  session.add(author)
  session.commit()
  return {"author": CreateAuthorOut(id=author.id, first_name=author.first_name, last_name=author.last_name)}