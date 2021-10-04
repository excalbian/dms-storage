from datetime import datetime, timedelta
from sqlalchemy.orm.session import sessionmaker


from typing import Optional, List
from .dbmodels import DbStorage, Storage, StorageStatus, User



# CRUD
# Should do:
# Prevent single slot from having multiple entires (slot_id/)
# Do basic reporting by user, by area, by slot, expiring, expired, etc
# 
class StorageAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def create_storage(self, storage:Storage) -> Storage:
        if storage.user.is_banned or not storage.user.is_active:
            raise UserCantReserve("User cannot reserve storage")

        with self._session() as db:
            reserved = db.query(DbStorage) \
                .filter( 
                    DbStorage.slot_id == storage.slot.id,
                    DbStorage.status != StorageStatus.closed
                ) \
                .all()

            if len(reserved) != 0:
                raise SlotAlreadyInUse("Slot already in use")
            
            if not storage.slot.enabled:
                raise SlotDisabled("Slot cannot be reserved")

            expiring = storage.expiring
            if expiring is None:
                expiring = datetime.now() + timedelta(days=storage.slot.storage_type.valid_days)

            s = DbStorage(
                user_id = storage.user.id,
                slot_id = storage.slot.id,
                started = storage.started,
                expiring = expiring,
                ended = storage.ended,
                status = storage.status             
            )

            db.add(s)
            db.commit()
            db.refresh(s)
            return Storage.from_orm(s)

    def get_storage_by_id(self, id: int) -> Storage:
        with self._session() as db:
            s = db.query(DbStorage).get(id)
            return None if s is None else  Storage.from_orm(s)
    
    def get_storage(
        self, 
        user: User = None, 
        only_active:bool = False,
        datefrom:Optional[datetime] = None,
        dateto:Optional[datetime] = None,
        limit:int = 100 ) -> List[Storage]:
        with self._session() as db:
            q = db.query(DbStorage)

            if user is not None:
                q = q.filter(DbStorage.user_id == user.id)
                
            if only_active:
                q = q.filter(DbStorage.status != StorageStatus.closed)
            
            if datefrom is not None:
                q = q.filter(DbStorage.started > datefrom)
            if dateto is not None:
                q = q.filter(DbStorage.started < dateto)

            q = q.order_by(DbStorage.started.desc()).limit(limit)
            return [Storage.from_orm(s) for s in q.all()]
    
    def get_all_active(self) -> List[Storage]:
         with self._session() as db:
            s = db.query(DbStorage) \
                .filter(DbStorage.status != StorageStatus.closed) \
                .all()
            return [Storage.from_orm(x) for x in s]
    
    def update(self, storage:Storage):
        with self._session() as db:
            rows = db.query(DbStorage) \
                .filter(DbStorage.id == storage.id) \
                .update({
                    DbStorage.started: storage.started,
                    DbStorage.expiring: storage.expiring,
                    DbStorage.ended: storage.ended,
                    DbStorage.status: storage.status  
                })
            db.commit()
            if rows <= 0:
                raise KeyError("Couldn't find storage with id {storage.id}")
            
            return Storage.from_orm( db.query(DbStorage).get(storage.id))
    



class SlotAlreadyInUse(Exception):
    pass

class SlotDisabled(Exception):
    pass

class UserCantReserve(Exception):
    pass

