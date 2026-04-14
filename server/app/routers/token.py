from datetime import timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from app.models import SessionDep, User, select, delete
from app.dependencies.authentication import get_user_from_refresh_token, hash_password, verify_password, create_access_token, create_refresh_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_refresh_token

router = APIRouter()

class TokenResponse(BaseModel):
  access_token: str
  token_type: str
  refresh_token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/token")
def token(request: LoginRequest, session: SessionDep) -> TokenResponse:
  user = session.exec(select(User).where(User.username == request.username)).first()
  if not user:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  if not verify_password(request.password, user.password):
    raise HTTPException(status_code=401, detail="Invalid credentials")

  refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=30))

  return TokenResponse(access_token=create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), token_type="bearer", refresh_token=refresh_token)

@router.post("/refresh-token")
def refresh_token(request: RefreshTokenRequest, session: SessionDep) -> TokenResponse:
  if not verify_refresh_token(request.refresh_token):
    raise HTTPException(status_code=401, detail="Invalid refresh token")
  user = get_user_from_refresh_token(request.refresh_token, session)
  refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=30))
  return TokenResponse(access_token=create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), token_type="bearer", refresh_token=refresh_token)

@router.post("/register")
def register(request: RegisterRequest, session: SessionDep) -> dict[str, str]:
  user = User(username=request.username, password=hash_password(request.password))
  try:
    session.add(user)
    session.commit()
  except IntegrityError as e:
    raise HTTPException(status_code=400, detail="Username already exists")
  return {"message": "User registered successfully", "user": str(user.id)}