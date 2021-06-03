from datetime import datetime
from . import DbBase
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from .storage_type import StorageType
from sqlalchemy.orm import relationship
from pydantic import BaseModel



class StorageSlot(DbBase):
    """ Storage Slot DB Model
        Represents a single reserveable place for storage.
    """
    __tablename__ = 'storage_slot'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    storage_type_id = Column(Integer, ForeignKey('storage_type.id'))
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    storage_type = relationship(StorageType.__name__)

# CRUD - basic crud, no delete
