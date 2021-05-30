from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel

class Permissions(Base):
    """ Permissions DB Model
        Permissions table for users that have beyond-base permissions. All
        users should have the ability to login and reserve storage when available (unless banned).
        This table is just for users that need admin, reportability, overrides, etc.
    """
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, unique=True)
    is_admin = Column(Boolean, default=False)
    can_report = Column(Boolean, default=False)
    can_configure = Column(Boolean, default=False)
    can_ban = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)