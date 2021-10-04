from datetime import datetime

from sqlalchemy.orm.session import sessionmaker
from .dbmodels import DbAuditLog, AuditLog, User

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