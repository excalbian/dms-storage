from datetime import datetime
from ntpath import join
from typing import List

from pydantic.fields import Field
from sqlalchemy.orm.session import sessionmaker
from . import DbBase, PydanticBase
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from .storage_type import StorageType, DbStorageType
from sqlalchemy.orm import relationship

class DbStorageSlot(DbBase):
    """ Storage Slot DB Model
        Represents a single reserveable place for storage.
    """
    __tablename__ = 'storage_slot'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    storage_type_id = Column(Integer, ForeignKey(DbStorageType.id))
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    storage_type = relationship(DbStorageType)

# CRUD - basic crud, no delete
class StorageSlot(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    name: str
    enabled: bool = True
    storage_type: StorageType

#CRUD - basic crud, no delete
class StorageSlotAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all(self) -> List[StorageSlot]:
         with self._session() as db:
            slots:List[DbStorageSlot] = db.query(DbStorageSlot) \
                .join(DbStorageType) \
                .order_by(DbStorageType.name, DbStorageSlot.name) \
                .all()
            return [StorageSlot.from_orm(s) for s in slots]
    
    def get_all_of_type(self, storage_type: StorageType) -> List[StorageSlot]:
        with self._session() as db:
            slots:List[DbStorageSlot] = db.query(DbStorageSlot) \
                .join(DbStorageType) \
                .filter(DbStorageSlot.storage_type_id == storage_type.id) \
                .order_by(DbStorageType.name, DbStorageSlot.name) \
                .all()
            return [StorageSlot.from_orm(s) for s in slots]
        
    def get_all_enabled(self) -> List[StorageType]:
        with self._session() as db:
            slots:List[DbStorageSlot] = db.query(DbStorageSlot) \
                .join(DbStorageType) \
                .filter(DbStorageSlot.enabled == True, DbStorageType.enabled == True) \
                .order_by(DbStorageSlot.storage_type, DbStorageSlot.name) \
                .all()
            return [StorageSlot.from_orm(s) for s in slots]

    def get_by_name(self, name: str, storage_type: StorageType = None) -> List[StorageSlot]:
        with self._session() as db:
            q = db.query(DbStorageSlot) \
                .join(DbStorageType) \
                .filter(DbStorageSlot.name == name)
            if storage_type is not None:
                q.filter(DbStorageSlot.storage_type_id == storage_type.id)
            
            slots = q.all()
                
            return [StorageSlot.from_orm(s) for s in slots]
    
    def get_by_id(self, id: int) -> StorageSlot:
        with self._session() as db:
            slot = db.query(DbStorageSlot).get(id)
            return None if slot is None else StorageSlot.from_orm(slot)
    
    def create(self, obj: StorageSlot) -> StorageSlot:
        with self._session() as db:
            s = DbStorageSlot(
                name=obj.name,
                storage_type_id = obj.storage_type.id,
                enabled=obj.enabled
            )
            
            db.add(s)
            db.commit()
            db.refresh(s)
            return StorageSlot.from_orm(s)
    
    def update(self, obj: StorageSlot) -> StorageSlot:
        with self._session() as db:

            u = db.query(DbStorageSlot).filter(DbStorageSlot.id == obj.id).update({ 
                DbStorageSlot.name: obj.name,
                DbStorageSlot.storage_type_id: obj.storage_type.id,
                DbStorageSlot.enabled: obj.enabled
            })
            if u <= 0:
                raise KeyError("StorageSlot with id {obj.id} not found")
            db.commit()
            updated = db.query(DbStorageSlot).get(obj.id)
            return StorageSlot.from_orm(updated)
    