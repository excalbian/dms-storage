from datetime import datetime
from typing import Optional
from app.database import Base
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, String, Text, JSON
from sqlalchemy.orm import relationship, Session
from . import PydanticBase

class User(Base):
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

class UserBase(PydanticBase):
    username: str
    displayname: Optional[str] = None
    phone: Optional[str] = None
    email: str
    next_use: Optional[datetime] = None
    class Config:
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    class Config:
        arbitrary_types_allowed = True

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime



class Crud():
    def __init__(self, db:Session):
        self._db = db
    
    def get_users(self, skip: int = 0, limit: int = 5000):
        return self._db.query(User) \
            .order_by(User.username) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def get_user_by_username(self, username: str):
        return self._db.query(User) \
            .filter(User.username == username) \
            .first()
    
    def create_user(self, obj: UserCreate) -> User:
        u = User(
            username = obj.username,
            displayname = obj.displayname,
            email = obj.email,
            phone = obj.phone,
            next_use = obj.next_use
        )
        
        self._db.add(u)
        self._db.commit()
        self._db.refresh(u)
        return u
    
    def update_user(self, obj: UserRead) -> User:
        u = self._db.query(User).get(obj.id).update(
        {
            User.email: obj.email,
            User.displayname: obj.displayname,
            User.phone: obj.phone,
            User.next_use: obj.next_use
        })
        self._db.commit()
        self._db.refresh(u)
        return u
