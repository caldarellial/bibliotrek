from datetime import timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from app.models import SessionDep, User, select, delete
from app.dependencies.authentication import hash_password, verify_password, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def token(request: LoginRequest, session: SessionDep) -> Token:
  user = session.exec(select(User).where(User.username == request.username)).first()
  if not user:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  if not verify_password(request.password, user.password):
    raise HTTPException(status_code=401, detail="Invalid credentials")

  return Token(access_token=create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), token_type="bearer")

@router.post("/register")
def register(request: RegisterRequest, session: SessionDep) -> dict[str, str]:
  user = User(username=request.username, password=hash_password(request.password))
  try:
    session.add(user)
    session.commit()
  except IntegrityError as e:
    raise HTTPException(status_code=400, detail="Username already exists")
  return {"message": "User registered successfully", "user": str(user.id)}