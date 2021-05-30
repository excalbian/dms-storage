from datetime import datetime
from app.database import Base
from .user import User
from .storage_slot import StorageSlot
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
class Storage(Base):
    """ Storage DB Model
        Represents a reservation of a storage slot. Main transactional table for the application
    """
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey('storage_slot.id'), nullable=False)
    started = Column(DateTime, default=datetime.now, nullable=False)
    expiring = Column(DateTime, nullable=True, index=True)
    ended = Column(DateTime, nullable=True)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    slot = relationship(StorageSlot.__name__)
    user = relationship(User.__name__, backref='storage')

