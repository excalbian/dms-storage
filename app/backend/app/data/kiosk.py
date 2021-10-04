from sqlalchemy.orm.session import sessionmaker
from .dbmodels import Kiosk, DbKiosk
from typing import List

# basic crud
class KioskAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all(self) -> List[Kiosk]:
        with self._session() as db:
            kiosks = db.query(DbKiosk).all()
            return [Kiosk.from_orm(k) for k in kiosks]
    
    def get_by_id(self, id: int) -> Kiosk:
        k:DbKiosk = None
        with self._session() as db:
            k = db.query(DbKiosk).get(id)
        return None if k is None else Kiosk.from_orm(k)

    def get_by_name(self, name: str) -> Kiosk:
        k:DbKiosk = None
        with self._session() as db:
            k = db.query(DbKiosk).filter(DbKiosk.name == name).first()
        return None if k is None else Kiosk.from_orm(k)

    def create(self, obj: Kiosk) -> Kiosk:
        with self._session() as db:
            k = DbKiosk(
                name = obj.name,
                printer_name = obj.printer_name
            )
            db.add(k)
            db.commit()
            db.refresh(k)
            return Kiosk.from_orm(k)

    def update(self, obj:Kiosk) -> Kiosk:
        with self._session() as db:
            k = db.query(DbKiosk) \
                .filter(DbKiosk.id == obj.id) \
                .update({
                    DbKiosk.name: obj.name,
                    DbKiosk.printer_name: obj.printer_name
                })
            if k <= 0:
                raise KeyError("Kiosk id {id} not found")
            return Kiosk.from_orm( db.query(DbKiosk).get(obj.id) )

    def delete(self, obj:Kiosk) -> None:
        with self._session() as db:
            k = db.query(DbKiosk).get(obj.id)
            if k is None:
                raise KeyError("Kiosk id {key} not found")
            db.delete(k)
            db.commit()