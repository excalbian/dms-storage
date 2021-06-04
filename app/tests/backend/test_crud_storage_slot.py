
from os import name
import app.backend.app.data.storage_type as storagetype
import app.backend.app.data.storage_slot as storageslot
from .fixtures import *
from app.tests.utils.randoms import random_string

def test_crud_create_get(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "Project Storage",
        location = "South Workshop",
        valid_days = 7
    )
    st = typeaccess.create(test_st)
    
    test_slot = storageslot.StorageSlot(
        name = "A-1",
        storage_type = st
    )

    created_slot = slotaccess.create(test_slot)
    retrieved_slot = slotaccess.get_by_id(created_slot.id)

    assert created_slot == retrieved_slot
    assert test_slot.name == retrieved_slot.name
    assert retrieved_slot.storage_type == st
    assert test_slot.enabled == True


def test_crud_get_by_name(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "Project Storage",
        location = "South Workshop",
        valid_days = 7
    )
    st = typeaccess.create(test_st)
    
    test_slot = storageslot.StorageSlot(
        name = "A-1",
        storage_type = st,
        enabled = True
    )
    created_slot = slotaccess.create(test_slot)
    retrieved_slot = slotaccess.get_by_name("A-1", storage_type=st)[0]


    assert created_slot == retrieved_slot
    assert test_slot.name == retrieved_slot.name
    assert retrieved_slot.storage_type == st
    assert test_slot.enabled == True

def test_crud_get_all(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "Project Storage",
        location = "South Workshop",
        valid_days = 7
    )
    st = typeaccess.create(test_st)
    
    test_slot = storageslot.StorageSlot(
        name = "B-0",
        storage_type = st,
        enabled = True
    )
    created_slot = slotaccess.create(test_slot)
    for i in range(0,99):
        slotaccess.create(storageslot.StorageSlot(
            name = "A-" + str(i),
            storage_type = st
        ))
    
    
    all_slots = slotaccess.get_all()

    assert len(all_slots) == 100
    assert created_slot == next((x for x in all_slots if x.id == created_slot.id), None)

def test_crud_get_by_type(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    st_types = [ 
        typeaccess.create(storagetype.StorageType(
        name = "Project Storage (S)",
        location = "South Workshop",
        valid_days = 7)),
        typeaccess.create(storagetype.StorageType(
        name = "Project Storage (N)",
        location = "North Workshop",
        valid_days = 7))
    ]
    

    
    test_slot = storageslot.StorageSlot(
        name = "B-0",
        storage_type = st_types[0],
        enabled = True
    )
    created_slot = slotaccess.create(test_slot)
    for i in range(0,99):
        slotaccess.create(storageslot.StorageSlot(
            name = "A-" + str(i),
            storage_type = st_types[i%2]
        ))
    
    
    all_slots = slotaccess.get_all_of_type(st_types[0])

    assert len(all_slots) == 51
    assert created_slot == next((x for x in all_slots if x.id == created_slot.id), None)

def test_crud_get_enabled(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    st_types = [ 
        typeaccess.create(storagetype.StorageType(
        name = "Project Storage (S)",
        location = "South Workshop",
        enabled = False,
        valid_days = 7)),
        typeaccess.create(storagetype.StorageType(
        name = "Project Storage (N)",
        location = "North Workshop",
        valid_days = 7))
    ]

    for i in range(0,100):
        slotaccess.create(storageslot.StorageSlot(
            name = "A-" + str(i),
            storage_type = st_types[i % 2],
            enabled = bool(int(i/50))
        ))
    
    
    all_slots = slotaccess.get_all_enabled()
    assert len(all_slots) == 25

def test_crud_update(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "Project Storage",
        location = "South Workshop",
        valid_days = 7
    )
    st = typeaccess.create(test_st)
    
    test_slot = storageslot.StorageSlot(
        name = "A-1",
        storage_type = st,
        enabled = True
    )
    created_slot = slotaccess.create(test_slot)
    created_slot.enabled = False
    updated_slot = slotaccess.update(created_slot)

    assert created_slot == updated_slot



def test_crud_bad_update(session):
    slotaccess = storageslot.StorageSlotAccess(session)
    typeaccess = storagetype.StorageTypeAccess(session)
    test_st = storagetype.StorageType(
        name = "Project Storage",
        location = "South Workshop",
        valid_days = 7
    )
    st = typeaccess.create(test_st)
    
    test_slot = storageslot.StorageSlot(
        name = "A-1",
        storage_type = st,
        enabled = True
    )

    with pytest.raises(KeyError):
        slotaccess.update(test_slot)
    
