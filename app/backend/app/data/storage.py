from datetime import datetime, timedelta
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Enum
from . import DbBase, PydanticBase
from .user import DbUser, User
from .storage_slot import DbStorageSlot, StorageSlot
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel, Field
from typing import Optional, List
import enum

class StorageStatus(str, enum.Enum):
    """ All types of statuses """
    pending = 'pending'
    active = 'active'
    expired = 'expired'
    closed = 'closed'

class DbStorage(DbBase):
    """ Storage DB Model
        Represents a reservation of a storage slot. Main transactional table for the application
    """
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey('storage_slot.id'), nullable=False)
    started = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(Enum(StorageStatus), default=StorageStatus.pending,  nullable=False)
    expiring = Column(DateTime, nullable=True, index=True)
    ended = Column(DateTime, nullable=True)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    slot = relationship(DbStorageSlot.__name__)
    user = relationship(DbUser.__name__, backref='storage')

# CRUD
# Should do:
# Prevent single slot from having multiple entires (slot_id/)
# Do basic reporting by user, by area, by slot, expiring, expired, etc
# 
class Storage(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    started: Optional[datetime]
    status: Optional[StorageStatus]
    expiring: Optional[datetime]
    ended: Optional[datetime]
    slot: StorageSlot
    user: User

class StorageAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def create_storage(self, storage:Storage) -> Storage:
        if storage.user.is_banned or not storage.user.is_active:
            raise UserCantReserve("User cannot reserve storage")

        with self._session() as db:
            reserved = db.query(DbStorage) \
                .filter( 
                    DbStorage.slot_id == storage.slot.id,
                    DbStorage.status != StorageStatus.closed
                ) \
                .all()

            if len(reserved) != 0:
                raise SlotAlreadyInUse("Slot already in use")
            
            if not storage.slot.enabled:
                raise SlotDisabled("Slot cannot be reserved")

            expiring = storage.expiring
            if expiring is None:
                expiring = datetime.now() + timedelta(days=storage.slot.storage_type.valid_days)

            s = DbStorage(
                user_id = storage.user.id,
                slot_id = storage.slot.id,
                started = storage.started,
                expiring = expiring,
                ended = storage.ended,
                status = storage.status             
            )

            db.add(s)
            db.commit()
            db.refresh(s)
            return Storage.from_orm(s)

    def get_storage_by_id(self, id: int) -> Storage:
        with self._session() as db:
            s = db.query(DbStorage).get(id)
            return None if s is None else  Storage.from_orm(s)
    
    def get_storage_by_user(self, user: User, only_active:bool = False) -> List[Storage]:
        with self._session() as db:
            q = db.query(DbStorage) \
                .filter(DbStorage.user_id == user.id)
                
            if only_active:
                q = q.filter(DbStorage.status != StorageStatus.closed)

            q.order_by(DbStorage.started.desc())
            return [Storage.from_orm(s) for s in q.all()]
    
    def get_all_active(self) -> List[Storage]:
         with self._session() as db:
            s = db.query(DbStorage) \
                .filter(DbStorage.status != StorageStatus.closed) \
                .all()
            return [Storage.from_orm(x) for x in s]
    
    def update(self, storage:Storage):
        with self._session() as db:
            rows = db.query(DbStorage) \
                .filter(DbStorage.id == storage.id) \
                .update({
                    DbStorage.started: storage.started,
                    DbStorage.expiring: storage.expiring,
                    DbStorage.ended: storage.ended,
                    DbStorage.status: storage.status  
                })
            db.commit()
            if rows <= 0:
                raise KeyError("Couldn't find storage with id {storage.id}")
            
            return Storage.from_orm( db.query(DbStorage).get(storage.id))
    



class SlotAlreadyInUse(Exception):
    pass

class SlotDisabled(Exception):
    pass

class UserCantReserve(Exception):
    pass

