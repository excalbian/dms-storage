from datetime import datetime
from . import DbBase
from sqlalchemy import Column, Integer, Enum, String, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
import enum

class HookType(str, enum.Enum):
    """ Types of webhooks available """
    slot_reserved = 'slot_reserved'
    slot_expired = 'slot_expired'
    slot_released = 'slot_released'
    slot_dead = 'slot_dead'
    user_banned = 'user_banned'

class Webhook(DbBase):
    """ Webhook DB Model
        Stores registered webhooks to fire when actions happen
    """
    id = Column(Integer, primary_key=True)
    type = Column(Enum(HookType), index=True)
    url = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # TODO: Authentication / Key storage

# CRUD - basic