from datetime import datetime
from app.appdef import db
import enum


class HookType(str, enum.Enum):
    """ Types of webhooks available """
    slot_reserved = 'slot_reserved'
    slot_expired = 'slot_expired'
    slot_released = 'slot_released'
    slot_dead = 'slot_dead'
    user_banned = 'user_banned'

class Webhook(db.Model):
    """ Webhook DB Model
        Stores registered webhooks to fire when actions happen
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(HookType), index=True)
    url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # TODO: Authentication / Key storage