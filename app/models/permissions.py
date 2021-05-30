from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel as PydanticBase
from typing import Optional

class Permissions(Base):
    """ Permissions DB Model
        Permissions table for users that have beyond-base permissions. All
        users should have the ability to login and reserve storage when available (unless banned).
        This table is just for users that need admin, reportability, overrides, etc.
    """
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, unique=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class _PermissionBase(PydanticBase):
    user_id: int
    is_admin: bool
    can_report: bool
    can_configure: bool
    can_ban: bool
    can_access: bool = True
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

class PermissionCreate(_PermissionBase):
    pass
class PermissionsRead(_PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime
class PermissionCrud():
    def __init__(self, db:Session):
        self._db = db
    
    def get_user_permissions(self, user_id: int):
        return self._db.query(Permissions) \
            .filter(Permissions.user_id==user_id) \
            .first()