from datetime import datetime

from sqlalchemy.sql.expression import null
from . import DbBase
from .user import User
from .storage_slot import StorageSlot
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
import enum

class StorageStatus(str, enum.Enum):
    """ All types of actions logged in the audit table """
    pending = 'pending'
    active = 'active'
    expired = 'expired'
    closed = 'closed'

class Storage(DbBase):
    """ Storage DB Model
        Represents a reservation of a storage slot. Main transactional table for the application
    """
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey('storage_slot.id'), nullable=False)
    started = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(StorageStatus, default=StorageStatus.active,  nullable=False)
    expiring = Column(DateTime, nullable=True, index=True)
    ended = Column(DateTime, nullable=True)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    slot = relationship(StorageSlot.__name__)
    user = relationship(User.__name__, backref='storage')

# CRUD
# Should do:
# Prevent single slot from having multiple entires (slot_id/)
# Do basic reporting by user, by area, by slot, expiring, expired, etc
# 