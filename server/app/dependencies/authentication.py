from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel
from app.config import get_settings
from uuid import UUID
from app.models import User, select, SessionDep

_settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()

SECRET_KEY = _settings.auth_secret_key or ""
if not _settings.auth_secret_key:
  raise ValueError("AUTH_SECRET_KEY is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: UUID

def create_access_token(data: dict, expires_delta: timedelta) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + expires_delta
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError as e:
        raise credentials_exception
    user = session.exec(select(User).where(User.id == token_data.id)).first()
    if user is None:
        raise credentials_exception
    return user
