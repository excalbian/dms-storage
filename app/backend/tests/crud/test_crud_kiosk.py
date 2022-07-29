
import app.data.kiosk as kiosk
from .fixtures import *
from ..utils.randoms import random_string

def test_crud_create_get(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )
    createdkiosk = access.create(testkiosk)
    retrievedkiosk = access.get_by_id(createdkiosk.id)

    assert createdkiosk == retrievedkiosk
    assert createdkiosk.name == testkiosk.name
    assert createdkiosk.printer_name == testkiosk.printer_name
    assert retrievedkiosk.name == testkiosk.name
    assert retrievedkiosk.printer_name == testkiosk.printer_name

def test_crud_get_by_name(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )
    createdkiosk = access.create(testkiosk)

    for i in range(0,99):
        access.create(kiosk.Kiosk(
            name = random_string(50),
            printer_name = random_string(75)
        ))
    
    
    retrievedkiosk = access.get_by_name("kiosk")

    assert createdkiosk == retrievedkiosk

def test_crud_get_all(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )
    createdkiosk = access.create(testkiosk)

    for i in range(0,99):
        access.create(kiosk.Kiosk(
            name = random_string(50),
            printer_name = random_string(75)
        ))
    kiosks = access.get_all()
    assert len(kiosks) == 100
    assert createdkiosk == next((x for x in kiosks if x.id == createdkiosk.id), None)

def test_crud_update(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )
    createdkiosk = access.create(testkiosk)
    createdkiosk.name = "newname"
    updatedkiosk = access.update(createdkiosk)

    assert createdkiosk == updatedkiosk
    assert updatedkiosk.name == "newname"

def test_crud_delete(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )
    createdkiosk = access.create(testkiosk)
    access.delete(createdkiosk)
    result = access.get_by_id(createdkiosk.id)

    assert result is None

def test_crud_bad_update(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )

    with pytest.raises(KeyError):
        access.update(testkiosk)
    
def test_crud_bad_delete(session):
    access = kiosk.KioskAccess(session)
    testkiosk = kiosk.Kiosk(
        name = "kiosk",
        printer_name = "print01"
    )

    with pytest.raises(KeyError):
        access.delete(testkiosk)
