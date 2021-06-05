from fastapi import Depends, HTTPException, status
from typing import Generator
from fastapi.security.oauth2 import OAuth2PasswordBearer

from sqlalchemy.orm.session import sessionmaker
from app.backend.app.core.database import get_db
from app.backend.app.data.user import User
from authlib.jose import jwt
from .token import Token 

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"login"
)

def get_current_user(
    db: sessionmaker = Depends(get_db), 
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, read_file('./app/jwtRS256.key.pub'))
        token_data = Token.parse_obj(payload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(ex))
    user = token_data
    if not user or not user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user