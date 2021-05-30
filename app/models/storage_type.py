from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel

class StorageType(Base):
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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
