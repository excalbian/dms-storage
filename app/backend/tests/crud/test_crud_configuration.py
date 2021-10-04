
from app.data.configuration import ConfigurationAccess
from .fixtures import *
from ..utils.randoms import random_string

def test_crud_create_get(session):
    configaccess = ConfigurationAccess(session)
    configaccess.create("testkey","testval")
    for i in range(0,999):
        configaccess.create(random_string(10),random_string(100))
    
    value = configaccess.get("testkey")
    all_values = configaccess.get_all_configuration()

    assert value == "testval"
    assert len(all_values) == 1000
    assert "testkey" in all_values

def test_crud_update(session):
    configaccess = ConfigurationAccess(session)
    configaccess.create("testkey","testval")
    configaccess.create("testkey2","nonsense")

    assert configaccess.get("testkey") == "testval"

    configaccess.update("testkey","anotherval")
    assert configaccess.get("testkey") == "anotherval"

def test_crud_delete(session):
    configaccess = ConfigurationAccess(session)
    configaccess.create("testkey","testval")
    configaccess.create("testkey2","nonsense")

    assert configaccess.get("testkey") == "testval"

    configaccess.delete("testkey")
    assert configaccess.get("testkey") is None

def test_crud_bad_delete(session):
    configaccess = ConfigurationAccess(session)
    configaccess.create("testkey","testval")
    with pytest.raises(KeyError):
        configaccess.delete("badkey")

def test_crud_bad_update(session):
    configaccess = ConfigurationAccess(session)
    configaccess.create("testkey","testval")
    with pytest.raises(KeyError):
        configaccess.update("badkey", "value")