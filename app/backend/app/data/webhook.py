from datetime import datetime
from typing import List

from pydantic.fields import Field
from sqlalchemy.orm.session import sessionmaker
from . import DbBase, PydanticBase
from sqlalchemy import Column, Integer, Enum, String, DateTime
import enum

class HookType(str, enum.Enum):
    """ Types of webhooks available """
    slot_reserved = 'slot_reserved'
    slot_expired = 'slot_expired'
    slot_released = 'slot_released'
    slot_dead = 'slot_dead'
    user_banned = 'user_banned'

class DbWebhook(DbBase):
    """ Webhook DB Model
        Stores registered webhooks to fire when actions happen
    """
    id = Column(Integer, primary_key=True)
    hooktype = Column(Enum(HookType), index=True)
    url = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # TODO: Authentication / Key storage

class Webhook(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    hooktype: HookType
    url: str

# CRUD - basic
class WebhookAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def create(self, obj:Webhook) -> Webhook:
        with self._session() as db:
            h = DbWebhook(
                hooktype = obj.hooktype,
                url = obj.url
            )
            
            db.add(h)
            db.commit()
            db.refresh(h)
            return Webhook.from_orm(h)

    def get_by_id(self, id:int) -> Webhook:
        with self._session() as db:
            h = db.query(DbWebhook).get(id)
            return None if h is None else Webhook.from_orm(h)

    def get_by_type(self, hooktype:HookType) -> List[Webhook]:
        with self._session() as db: 
            hooks = db.query(DbWebhook).filter(DbWebhook.hooktype == hooktype).all()
            return [Webhook.from_orm(h) for h in hooks]

    def update(self, hook:Webhook) -> Webhook:
       with self._session() as db:
            rows = db.query(DbWebhook) \
                .filter(DbWebhook.id == hook.id) \
                .update({
                    DbWebhook.hooktype: hook.hooktype,
                    DbWebhook.url: hook.url 
                })
            
            if rows <= 0:
                raise KeyError("Couldn't find Webhook with id {hook.id}")
            db.commit()
            return Webhook.from_orm( db.query(DbWebhook).get(hook.id))
    


    def delete(self, hook:Webhook) -> None:
        with self._session() as db:
            h = db.query(DbWebhook).get(hook.id)
            if h is None:
                raise KeyError("Webhook id {hook.id} not found")
            db.delete(h)
            db.commit()