from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.logger import logger

from starlette.requests import Request

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