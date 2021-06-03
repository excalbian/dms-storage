from datetime import datetime

from sqlalchemy.orm.session import sessionmaker
from . import DbBase
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from app.backend.app.core.database import get_db
from . import PydanticBase
from pydantic import Field
from typing import Optional

class DbConfiguration(DbBase):
    """ Configuration DB class
        Represents simple key/value configuration entries for the application. Meant
        to be read once and cached.
    """
    id = Column(Integer, primary_key=True)
    key = Column(String(25), index=True, unique=True)
    value = Column(Text)

# basic crud
class ConfigurationAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all_configuration(self) -> dict:
        with self._session() as db:
            q = db.query(DbConfiguration).all()
            return { c.key:c.value for c in q }
    
    def get(self, key: str) -> str:
        c:DbConfiguration = None
        with self._session() as db:
            c = db.query(DbConfiguration).filter(DbConfiguration.key == key).first()
        return None if c is None else c.value

    def create(self, key: str, value: str) -> None:
        with self._session() as db:
            c = DbConfiguration(
                key = key,
                value = value
            )
            
            db.add(c)
            db.commit()
            return

    def update(self, key: str, value: str) -> None:
        with self._session() as db:
            c = db.query(DbConfiguration) \
                .filter(DbConfiguration.key == key) \
                .update({DbConfiguration.value:value})
            if c <= 0:
                raise KeyError("{key} not found")
            db.commit()


    def delete(self, key: str) -> None:
        with self._session() as db:
            c = db.query(DbConfiguration).filter(DbConfiguration.key == key).first()
            if c is None:
                raise KeyError("{key} not found")
            db.delete(c)
            db.commit()
        
    
    