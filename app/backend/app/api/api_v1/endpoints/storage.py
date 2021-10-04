
from typing import Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.logger import logger
from pydantic.main import BaseModel
from sqlalchemy.sql.sqltypes import Integer

from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.api  import deps
from app.core.settings import settings
from app.data.dbmodels import AuditLog, AuditType, User
from app.data.storage import SlotAlreadyInUse, SlotDisabled, StorageAccess, Storage, StorageStatus, UserCantReserve
from app.data.storage_slot import StorageSlotAccess
from app.data.auditlog import AuditLogAccess
from app.data.user import UserAccess

from app.core.database import SessionLocal
#import logging

router = APIRouter()
#logger = logging.getLogger(__name__)


@router.get('/storage/{storage_id}')
async def get_storage_by_id(
    request: Request, 
    storage_id: int,
    user:User = Depends(deps.get_current_active_user) ):
    
    access = StorageAccess(SessionLocal)
    storage = access.get_storage_by_id(storage_id)
    if( storage is None ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif( storage.user.id == user.id 
        or user.is_admin ):
        return storage
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



class RequestStorage(BaseModel):
    userid: int
    slotid: int


@router.post('/storage')
async def allocate_storage(
    request: RequestStorage,
    user:User = Depends(deps.get_current_active_user) ):
    # TODO: Need lots of logic to check if user is allowed to add a new storage reservation
    # For instance, did they fill out the quiz, are they banned, is it too soon, etc?
    # Admins should be able to add anybody though, regardless of statuses

    storage_access = StorageAccess(SessionLocal)
    slot_access = StorageSlotAccess(SessionLocal)
    user_access = UserAccess(SessionLocal)
    audit_access = AuditLogAccess(SessionLocal)
    storage_user = user 

    
    # Check for user_id lookup, and only allow admin to do other users
    if user.id != request.userid:
        if not user.is_admin:
            audit_access.create(AuditLog(
                logtype=AuditType.security, 
                user = user,
                message=f'User {user.username} attempted to reserve for {request.userid} but was not admin')
            )
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Cannot reserve for other users")
        else:
            storage_user = user_access.get_user_by_id(request.userid)
            if(storage_user is None):
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST)
            
    slot = slot_access.get_by_id(request.slotid)

    try:
        storage = Storage(
            status = StorageStatus.active,
            slot = slot,
            user = storage_user
        )
        storage = storage_access.create_storage(storage)
        audit_access.create(AuditLog(
                logtype=AuditType.slotreserved, 
                data={'slot_id': request.slotid, 'foruser': storage_user.dict()},
                user=user)
            )
    except (SlotAlreadyInUse, SlotDisabled):
        # Data layer kicked it back because slot is in use or disabled
        raise HTTPException(detail="Slot not available", status_code=HTTP_409_CONFLICT)
    except UserCantReserve:
        # Data layer says user isn't allowed. Probably should check outselves before this point
        audit_access.create(AuditLog(
            logtype=AuditType.security, 
            user = user,
            message=f'User {user.username} attempted to reserve but was forbidden',
            data=user.dict()
        ))
        raise HTTPException(detail="User can't reserve", status_code=HTTP_403_FORBIDDEN)

    # return what was created
    return storage

@router.get("/storage")
async def get_storage(
    userid: Optional[int] = None,
    user:User = Depends(deps.get_current_active_user) 
):

    lookupuser:User = user
    
    # Switch to userid if applicable
    if( userid is not None and user.id != userid ):
        if( not user.is_admin):
            raise HTTPException(detail="Cannot retrive other users", status_code=HTTP_403_FORBIDDEN)
        else:
            useraccess = UserAccess(SessionLocal)
            lookupuser = useraccess.get_user_by_id(userid)
            if( lookupuser is None):
                raise HTTPException(detail="User not found", status_code=HTTP_404_NOT_FOUND)
    
    storage_access = StorageAccess(SessionLocal)
    return storage_access.get_storage(user = lookupuser)
