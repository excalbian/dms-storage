from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from .storage_type import StorageType
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel



class StorageSlot(Base):
    """ Storage Slot DB Model
        Represents a single reserveable place for storage.
    """
    __tablename__ = 'storage_slot'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    storage_type_id = Column(Integer, ForeignKey('storage_type.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    storage_type = relationship(StorageType.__name__)
