from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID
from app.models import Author, SessionDep

router = APIRouter(prefix="/authors")

class CreateAuthorOut(BaseModel):
  id: UUID
  name: str

@router.post("/")
def create_author(author: Author, session: SessionDep) -> dict[str, CreateAuthorOut]:
  session.add(author)
  session.commit()
  return {"author": CreateAuthorOut(id=author.id, name=author.name)}