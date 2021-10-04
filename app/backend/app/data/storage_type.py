from sqlalchemy.orm.session import sessionmaker
from .dbmodels import DbStorageType, StorageType
from typing import List



#CRUD - basic crud, no delete
class StorageTypeAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all(self) -> List[StorageType]:
        with self._session() as db:
            storage_types:List[DbStorageType] = db.query(DbStorageType) \
                .order_by(DbStorageType.name) \
                .all()
        
            return [ StorageType.from_orm(u) for u in storage_types ]
        
    def get_enabled(self) -> List[StorageType]:
        with self._session() as db:
            storage_types:List[DbStorageType] = db.query(DbStorageType) \
                .filter(DbStorageType.enabled == True) \
                .order_by(DbStorageType.name) \
                .all()
        
            return [ StorageType.from_orm(u) for u in storage_types ]

    def get_by_name(self, name: str) -> StorageType:
        with self._session() as db:
            db_storage_type = db.query(DbStorageType) \
                .filter(DbStorageType.name == name) \
                .first()
            st = StorageType.from_orm(db_storage_type)
            return st
    
    def get_by_id(self, id: int) -> StorageType:
        with self._session() as db:
            db_storage_type = db.query(DbStorageType).get(id)
            return None if db_storage_type is None else StorageType.from_orm(db_storage_type)
    
    def create(self, obj: StorageType) -> StorageType:
        with self._session() as db:
            d = {
                key:value for key,value in obj.dict().items() \
                if key not in ['id', 'created_at','updated_at']
            }
            st = DbStorageType(**d)
            
            db.add(st)
            db.commit()
            db.refresh(st)
            return StorageType.from_orm(st)
    
    def update(self, obj: StorageType) -> StorageType:
        with self._session() as db:
            d = {
                key:value for key,value in obj.dict().items() \
                if key not in ['id', 'created_at','updated_at']
            }
            u = db.query(DbStorageType).filter(DbStorageType.id == obj.id).update(d)
            if u <= 0:
                raise KeyError("StorageType with id {obj.id} not found")
            db.commit()
            updated = db.query(DbStorageType).get(obj.id)
            return StorageType.from_orm(updated)
    