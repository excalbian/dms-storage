
from os import name
import app.backend.app.data.storage_type as storagetype
from .fixtures import *
from app.tests.utils.randoms import random_string

def test_crud_create_get(session):
    access = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "storagetype",
        location = "dms",
        valid_days = 7
    )
    created_st = access.create(test_st)
    retrieved_st = access.get_by_id(created_st.id)

    assert created_st == retrieved_st
    assert test_st.name == retrieved_st.name
    assert test_st.location == retrieved_st.location
    assert test_st.valid_days == retrieved_st.valid_days
    assert True == retrieved_st.enabled

def test_crud_get_by_name(session):
    access = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "storagetype",
        location = "dms",
        valid_days = 7
    )
    created_st = access.create(test_st)
    retrieved_st = access.get_by_name(test_st.name)

    assert created_st == retrieved_st

def test_crud_get_all(session):
    access = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "storagetype",
        location = "dms",
        valid_days = 7
    )
    created_st = access.create(test_st)

    for i in range(0,99):
        access.create(storagetype.StorageType(
            name = random_string(25),
            location = random_string(20),
            valid_days = 30
        ))
    all_types = access.get_all()
    assert len(all_types) == 100
    assert created_st == next((x for x in all_types if x.id == created_st.id), None)

def test_crud_update(session):
    access = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "storagetype",
        location = "dms",
        valid_days = 7
    )
    created_st = access.create(test_st)
    created_st.name = "newname"
    updated_st = access.update(created_st)

    assert created_st == updated_st
    assert updated_st.name == "newname"


def test_crud_bad_update(session):
    access = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "storagetype",
        location = "dms",
        valid_days = 7
    )

    with pytest.raises(KeyError):
        access.update(test_st)
    
