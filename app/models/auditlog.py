from datetime import datetime
from typing import Optional
from .user import User
from app.database import Base
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, Session
import enum
from . import PydanticBase

class AuditType(str, enum.Enum):
    """ All types of actions logged in the audit table """
    login = 'login'
    slotreserved = 'slotreserved'
    slotreleased = 'slotreleased'
    userupdated = 'userupdated'
    reportrun = 'reportrun'
    slotupdated = 'slotupdated'

class AuditLog(Base):
    """ Represents an audit entry in the database. Used for all
        actions that should be auditable """
    __tablename__ = "auditlog"
    id = Column(Integer, primary_key=True)
    logtime = Column(DateTime, default=datetime.now)
    type = Column(Enum(AuditType))
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(Text)
    data = Column(JSON)
    user = relationship(User.__name__)


class AuditLogBase(PydanticBase):
    type: AuditType
    message: str
    data: Optional[str] = None
    user: User

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    id: int
    logtime: datetime

    class Config:
        orm_mode = True

class Crud():
    def __init__(self, db: Session):
        self._db = db

    def get_logs(self, date_from: datetime, date_to: datetime, skip: int = 0, limit: int = 5000):
        q = self._db.query(AuditLog)
        if( date_from is not None ):
            q = q.filter(AuditLog.logtime >= date_from)
        if( date_to is not None ):
            q = q.filter(AuditLog.logtime <= date_to)
        return q \
            .order_by(AuditLog.logtime.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def get_user_logs(self, user: User, skip: int = 0, limit: int = 5000):
        return self._db.query(AuditLog) \
            .filter( AuditLog.user_id == user.id ) \
            .order_by(AuditLog.logtime.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()
    
    def create_log(self, obj: AuditLogCreate) -> AuditLog:
        log = AuditLog( 
            type = obj.type,
            user_id = obj.user.id,
            message = obj.message,
            data = obj.data )
        
        self._db.add(log)
        self._db.commit()
        self._db.refresh(log)
        return log