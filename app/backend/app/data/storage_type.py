from datetime import datetime
from typing import List, Optional
from pydantic.fields import Field

from sqlalchemy.orm.session import sessionmaker
from . import DbBase, PydanticBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel

class DbStorageType(DbBase):
    """ StorageType DB Model
        Represents a type of storage - e.g. flex area vertical, flex area shelf, 
        warehouse large shelf, ikea tub, etc. Should have a name and a location, but is 
        not a reservable space - that is a storage slot.
    """
    __tablename__ = 'storage_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    location = Column(String(30), nullable=True)
    valid_days = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class StorageType(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    name: str
    location: str
    valid_days: Optional[int]
    enabled: bool = True

#CRUD - basic crud, no delete
class StorageTypeAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all(self) -> List[StorageType]:
        with self._session() as db:
            storage_types:List[DbStorageType] = db.query(DbStorageType) \
                .order_by(DbStorageType.name) \
                .all()
        
            return [ StorageType.from_orm(u) for u in storage_types ]
        
    def get_enabled(self) -> List[StorageType]:
        with self._session() as db:
            storage_types:List[DbStorageType] = db.query(DbStorageType) \
                .filter(DbStorageType.enabled == True) \
                .order_by(DbStorageType.name) \
                .all()
        
            return [ StorageType.from_orm(u) for u in storage_types ]

    def get_by_name(self, name: str) -> StorageType:
        with self._session() as db:
            db_storage_type = db.query(DbStorageType) \
                .filter(DbStorageType.name == name) \
                .first()
            st = StorageType.from_orm(db_storage_type)
            return st
    
    def get_by_id(self, id: int) -> StorageType:
        with self._session() as db:
            db_storage_type = db.query(DbStorageType).get(id)
            return None if db_storage_type is None else StorageType.from_orm(db_storage_type)
    
    def create(self, obj: StorageType) -> StorageType:
        with self._session() as db:
            d = {
                key:value for key,value in obj.dict().items() \
                if key not in ['id', 'created_at','updated_at']
            }
            st = DbStorageType(**d)
            
            db.add(st)
            db.commit()
            db.refresh(st)
            return StorageType.from_orm(st)
    
    def update(self, obj: StorageType) -> StorageType:
        with self._session() as db:
            d = {
                key:value for key,value in obj.dict().items() \
                if key not in ['id', 'created_at','updated_at']
            }
            u = db.query(DbStorageType).filter(DbStorageType.id == obj.id).update(d)
            if u <= 0:
                raise KeyError("StorageType with id {obj.id} not found")
            db.commit()
            updated = db.query(DbStorageType).get(obj.id)
            return StorageType.from_orm(updated)
    