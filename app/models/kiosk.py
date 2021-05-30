from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel



class Kiosk(Base):
    """ Kiosk DB Model
        Meant to represent an address or machine name of a kiosk, to 
        automatically put it in a kiosk mode. The printer name will
        be used to connect and print out tags when necessary.
    """
    __tablename__ = 'kiosk'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    printer_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)