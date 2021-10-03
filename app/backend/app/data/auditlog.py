from datetime import datetime
from typing import Optional

from sqlalchemy.orm.session import sessionmaker
from .user import DbUser, User
from . import DbBase
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, Session
import enum
from . import PydanticBase
from pydantic import Field

class AuditType(str, enum.Enum):
    """ All types of actions logged in the audit table """
    login = 'login'
    slotreserved = 'slotreserved'
    slotreleased = 'slotreleased'
    userupdated = 'userupdated'
    reportrun = 'reportrun'
    slotupdated = 'slotupdated'
    security = 'security'
    info = 'info'

class DbAuditLog(DbBase):
    """ Represents an audit entry in the database. Used for all
        actions that should be auditable """
    __tablename__ = 'auditlog'
    id = Column(Integer, primary_key=True)
    logtime = Column(DateTime, default=datetime.now)
    logtype = Column(Enum(AuditType))
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(Text)
    data = Column(JSON)
    user = relationship(DbUser.__name__)


class AuditLog(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    logtime: datetime = Field(allow_mutation=False, default=datetime.min)
    logtype: AuditType = AuditType.info
    message: str = ""
    data: Optional[dict] = None
    user: User

class AuditLogAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm

    def get_by_date(self, date_from: datetime, date_to: datetime, skip: int = 0, limit: int = 5000):
        with self._session() as db:
            q = db.query(DbAuditLog)
            if( date_from is not None ):
                q = q.filter(DbAuditLog.logtime >= date_from)
            if( date_to is not None ):
                q = q.filter(DbAuditLog.logtime <= date_to)
            logs = q.order_by(DbAuditLog.logtime.desc()) \
                .offset(skip) \
                .limit(limit) \
                .all()
            return [AuditLog.from_orm(l) for l in logs ]

    def get_by_user(self, user: User, skip: int = 0, limit: int = 5000):
        with self._session() as db:
            logs = db.query(DbAuditLog) \
            .filter( DbAuditLog.user_id == user.id ) \
            .order_by(DbAuditLog.logtime.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

            return [AuditLog.from_orm(l) for l in logs ]
    
    def create(self, obj: AuditLog) -> AuditLog:
        with self._session() as db:
            log = DbAuditLog( 
                logtype = obj.logtype,
                user_id = obj.user.id,
                message = obj.message,
                data = obj.data )
            
            db.add(log)
            db.commit()
            db.refresh(log)
            return AuditLog.from_orm(log)