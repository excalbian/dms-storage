from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.logger import logger

from starlette.requests import Request

from app.api  import deps
from app.core.settings import settings
from app.data.dbmodels import AuditLog, AuditType, User
from app.data.user import UserAccess
from app.data.auditlog import AuditLogAccess
from app.core.security import create_access_token, ad_auth_user
from app.core.database import SessionLocal


from datetime import timedelta, datetime
#import logging

router = APIRouter()
#logger = logging.getLogger(__name__)

@router.post('/auth')
async def auth(
    request: Request, 
    form_data: OAuth2PasswordRequestForm = Depends()):

    username = form_data.username
    password = form_data.password
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = None
    try:
        logger.debug(f'User logging in {username}')
        user = ad_auth_user(username, password)
        logger.debug(f'Got user from AD: {username}, {user["name"]}, {user["email"]}')
    except:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
   
    user_access = UserAccess(SessionLocal)
    audit_log_access = AuditLogAccess(SessionLocal)
    dbuser = user_access.get_user_by_username(user['username'])
    if dbuser is None:
        newuser = User(
            username = user['username'], 
            email = user['email'], 
            displayname = user['name'])
        dbuser = user_access.create_user(newuser)
        audit_log_access.create( AuditLog(
            logtime=datetime.now(),
            logtype=AuditType.login,
            message=f'New user {user["name"]} created.',
            data=None,
            user=dbuser
        ))
        logger.info(f'Created new database user {dbuser.id} for {username}')
    logger.debug(f'User {username} logged in as {dbuser.id}')
    audit_log_access.create( AuditLog(
            logtime=datetime.now(),
            logtype=AuditType.login,
            message=f'',
            data=None,
            user=dbuser
        ))
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": create_access_token(
            dbuser.id,
            expires_delta=access_token_expires,
            user=dbuser
        ),
        "token_type": "bearer",
    }




