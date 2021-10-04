
from .fixtures import *
from ..utils.randoms import random_string

from app.data.dbmodels import Webhook, HookType
from app.data.webhook import WebhookAccess

def test_crud_create_get(session):
    access = WebhookAccess(session)
    testhook = Webhook(
        hooktype = HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    retrieved = access.get_by_id(created.id)

    assert created == retrieved
    assert retrieved.hooktype == testhook.hooktype
    assert retrieved.url == retrieved.url

def test_crud_get_bad_id(session):
    access = WebhookAccess(session)
    retrieved = access.get_by_id(-100)
    assert retrieved is None


def test_crud_get_by_type(session):
    access = WebhookAccess(session)
    types = [HookType.slot_dead, HookType.slot_expired]
    for i in range(0,100):
        access.create(Webhook(
            hooktype = types[i%2],
            url = random_string(100)
        ))

    results = access.get_by_type(HookType.slot_dead)

    assert len(results) == 50

def test_crud_update(session):
    access = WebhookAccess(session)
    testhook = Webhook(
        hooktype = HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    created.hooktype = HookType.slot_dead
    result = access.update(created)
    assert created == result

def test_crud_delete(session):
    access = WebhookAccess(session)
    testhook = Webhook(
        hooktype = HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    retrieved = access.get_by_id(created.id)
    access.delete(retrieved)
    result = access.get_by_id(created.id)

    assert retrieved is not None
    assert result is None

def test_crud_bad_update(session):
    access = WebhookAccess(session)
    testhook = Webhook(
        hooktype = HookType.slot_reserved,
        url = random_string(100)
    )

    with pytest.raises(KeyError):
        access.update(testhook)
    
def test_crud_bad_delete(session):
    access = WebhookAccess(session)
    testhook = Webhook(
        hooktype = HookType.slot_reserved,
        url = random_string(100)
    )

    with pytest.raises(KeyError):
        access.delete(testhook)
