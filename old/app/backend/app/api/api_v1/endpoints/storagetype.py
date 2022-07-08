from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.logger import logger

from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND

from app.api  import deps
from app.core.settings import settings
from app.data.storage_type import StorageTypeAccess, StorageType
from app.data.user import User
from app.core.database import SessionLocal

from datetime import timedelta
#import logging

router = APIRouter()
#logger = logging.getLogger(__name__)

@router.get('/storagetype')
async def getStorageTypes(
    request: Request, 
    user:User = Depends(deps.get_current_active_user)):
    
    stAccess = StorageTypeAccess(SessionLocal)
    return stAccess.get_enabled()

@router.get('/storagetype/{storagetype_id}')
async def get_storage_type(
    request: Request, 
    storagetype_id: int,
    user:User = Depends(deps.get_current_active_user)):
    
    access = StorageTypeAccess(SessionLocal)
    t = access.get_by_id(storagetype_id)
    if t is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return t

@router.post('/storagetype')
async def post_storage_type():
    pass

