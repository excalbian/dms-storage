from typing import Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.logger import logger
from pydantic.main import BaseModel

from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.api  import deps
from app.core.settings import settings
from app.data.dbmodels import User
from app.data.storage_slot import StorageSlot, StorageSlotAccess
from app.data.storage_type import StorageTypeAccess
from app.core.database import SessionLocal


#import logging

router = APIRouter()
#logger = logging.getLogger(__name__)

@router.get('/storageslot')
async def get_slots(
    request: Request, 
    storagetype_id: Optional[int] = None,
    all: bool = False,
    user:User = Depends(deps.get_current_active_user)):
    
    slot_access = StorageSlotAccess(SessionLocal)
    type_access = StorageTypeAccess(SessionLocal)

    if all and not ( user.is_admin or user.can_configure):
        raise HTTPException(detail="Not allowed to retrieve all", status_code=HTTP_403_FORBIDDEN)
    
    if storagetype_id is not None:
        st_type = type_access.get_by_id(storagetype_id)
        if st_type is None:
            raise HTTPException(detail='Storage type not found', status_code=HTTP_400_BAD_REQUEST)
        return slot_access.get_all_of_type(storage_type=st_type, enabled_only=True)
    else:
        return slot_access.get_all_enabled()

    

@router.get('/storageslot/{slot_id}')
async def get_storage_slot(
    request: Request,
    slot_id: int,
    user:User = Depends(deps.get_current_active_user)
):
    slot_access = StorageSlotAccess(SessionLocal)
    slot = slot_access.get_by_id(slot_id)
    if slot is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    return slot

class RequestSlot(BaseModel):
    name: str
    storage_type_id: int

@router.post('/storageslot')
async def post_storage_slot(
    request: Request,
    slot: RequestSlot,
    user:User = Depends(deps.get_current_active_configuser)
):
    slot_access = StorageSlotAccess(SessionLocal)
    type_access = StorageTypeAccess(SessionLocal)

    t = type_access.get_by_id(slot.storage_type_id)
    if t is None:
        raise HTTPException(detail="Storage Type not found", status_code=HTTP_400_BAD_REQUEST)
    
    new_slot = slot_access.create(
        StorageSlot(
            name = slot.name,
            storage_type = t
        )
    )

    return new_slot