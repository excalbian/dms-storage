from typing import List

from sqlalchemy.orm.session import sessionmaker
from .dbmodels import DbWebhook, HookType, Webhook




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