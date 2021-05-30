from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel


class Configuration(Base):
    """ Configuration DB class
        Represents simple key/value configuration entries for the application. Meant
        to be read once and cached.
    """
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), index=True, unique=True)
    value = Column(Text)
