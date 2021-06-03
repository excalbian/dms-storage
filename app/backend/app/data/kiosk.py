from datetime import datetime
from typing import Optional
from pydantic.fields import Field

from sqlalchemy.orm.session import sessionmaker
from . import DbBase
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from typing import List
from . import PydanticBase


class DbKiosk(DbBase):
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

class Kiosk(PydanticBase):
    id: int = Field(allow_mutation=False)
    name: str
    printer_name = Optional[str]

# basic crud
class AuditLogAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_all(self) -> List[Kiosk]:
        with self._session() as db:
            kiosks = db.query(DbKiosk).all()
            return [Kiosk.from_orm(k) for k in kiosks]
    
    def get_by_id(self, id: int) -> Kiosk:
        c:DbKiosk = None
        with self._session() as db:
            k = db.query(DbKiosk).get(id)
        return None if c is None else Kiosk.from_orm(k)

    def get_by_name(self, name: str) -> Kiosk:
        c:DbKiosk = None
        with self._session() as db:
            k = db.query(DbKiosk).filter(DbKiosk.name == name).first()
        return None if c is None else Kiosk.from_orm(k)

    def create(self, obj: Kiosk) -> None:
        with self._session() as db:
            k = DbKiosk(**obj.dict())
            db.add(k)
            db.commit()
            return

    def update(self, obj:Kiosk) -> None:
        with self._session() as db:
            k = db.query(DbKiosk).get(obj.id)
            if k is None:
                raise KeyError("Kiosk id {id} not found")
            k.update({
                DbKiosk.name: obj.name,
                DbKiosk.printer_name: obj.printer_name
            })
            db.commit()

    def delete(self, obj:Kiosk) -> None:
        with self._session() as db:
            k = db.query(DbKiosk).get(obj.id)
            if k is None:
                raise KeyError("Kiosk id {key} not found")
            db.delete(k)
            db.commit()