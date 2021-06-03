from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm.session import sessionmaker
from . import DbBase
from app.backend.app.core.database import get_db
from sqlalchemy import Column, Boolean, Integer, DateTime, String
from sqlalchemy.orm import relationship
from . import PydanticBase
from pydantic import Field

class DbUser(DbBase):
    """ User DB Model
        While not the authoritative source for login, as we'll use OAuth for that,
        this model storage basic information about those users for use with this
        system.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True, unique=True)
    displayname = Column(String(100))
    phone = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    next_use = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    can_report = Column(Boolean, default=False)
    can_configure = Column(Boolean, default=False)
    can_ban = Column(Boolean, default=False)


class User(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    username: str
    displayname: Optional[str] = None
    phone: Optional[str] = None
    email: str
    is_active: bool = True
    is_banned: bool = False
    is_admin: bool = False
    can_report: bool = False
    can_configure: bool = False
    can_ban: bool = False
    next_use: Optional[datetime] = None

class UserAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_users(self, skip: int = 0, limit: int = 5000) -> List[User]:
        with self._session() as db:
            users:List[DbUser] = db.query(DbUser) \
                .order_by(DbUser.username) \
                .offset(skip) \
                .limit(limit) \
                .all()
        
            return [ User.from_orm(u) for u in users ]
        

    def get_user_by_username(self, username: str) -> User:
        with self._session() as db:
            dbuser = db.query(DbUser) \
                .filter(DbUser.username == username) \
                .first()
            user = User.from_orm(dbuser)
            return user
    
    def create_user(self, obj: User) -> User:
        with self._session() as db:
            u = DbUser(
                username = obj.username,
                displayname = obj.displayname,
                email = obj.email,
                phone = obj.phone,
                next_use = obj.next_use
            )
            
            db.add(u)
            db.commit()
            db.refresh(u)
            return User.from_orm(u)
    
    def update_user(self, obj: User) -> User:
        with self._session() as db:
            u = db.query(DbUser).filter(DbUser.id == obj.id) \
            .update(
            {
                DbUser.email: obj.email,
                DbUser.displayname: obj.displayname,
                DbUser.phone: obj.phone,
                DbUser.next_use: obj.next_use,
                DbUser.is_active: obj.is_active,
                DbUser.is_banned: obj.is_banned,
                DbUser.is_admin: obj.is_admin,
                DbUser.can_report: obj.can_report,
                DbUser.can_configure: obj.can_configure,
                DbUser.can_ban: obj.can_ban  
            })
            if u <= 0:
                raise KeyError("User with id {obj.id} not found")
            db.commit()
            updated = db.query(DbUser).get(obj.id)
            return User.from_orm(updated)
    
