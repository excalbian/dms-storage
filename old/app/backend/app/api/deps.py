from fastapi import Depends, HTTPException, status
from typing import Generator
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.api.api_v1.endpoints.auth import router

from sqlalchemy.orm.session import sessionmaker
from app.core.database import get_db
from app.data.user import User
from app.core.security import get_user_from_token
from authlib.jose import jwt
from .token import Token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")

def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        user = get_user_from_token(token)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(ex))
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

def get_current_active_configuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user is None or (
        current_user.is_admin != True 
        and current_user.can_configure != True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user