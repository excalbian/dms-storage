
import app.backend.app.data.webhook as webhook
from .fixtures import *
from app.tests.utils.randoms import random_string

def test_crud_create_get(session):
    access = webhook.WebhookAccess(session)
    testhook = webhook.Webhook(
        hooktype = webhook.HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    retrieved = access.get_by_id(created.id)

    assert created == retrieved
    assert retrieved.hooktype == testhook.hooktype
    assert retrieved.url == retrieved.url

def test_crud_get_bad_id(session):
    access = webhook.WebhookAccess(session)
    retrieved = access.get_by_id(-100)
    assert retrieved is None


def test_crud_get_by_type(session):
    access = webhook.WebhookAccess(session)
    types = [webhook.HookType.slot_dead, webhook.HookType.slot_expired]
    for i in range(0,100):
        access.create(webhook.Webhook(
            hooktype = types[i%2],
            url = random_string(100)
        ))

    results = access.get_by_type(webhook.HookType.slot_dead)

    assert len(results) == 50

def test_crud_update(session):
    access = webhook.WebhookAccess(session)
    testhook = webhook.Webhook(
        hooktype = webhook.HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    created.hooktype = webhook.HookType.slot_dead
    result = access.update(created)
    assert created == result

def test_crud_delete(session):
    access = webhook.WebhookAccess(session)
    testhook = webhook.Webhook(
        hooktype = webhook.HookType.slot_reserved,
        url = random_string(100)
    )
    created = access.create(testhook)
    retrieved = access.get_by_id(created.id)
    access.delete(retrieved)
    result = access.get_by_id(created.id)

    assert retrieved is not None
    assert result is None

def test_crud_bad_update(session):
    access = webhook.WebhookAccess(session)
    testhook = webhook.Webhook(
        hooktype = webhook.HookType.slot_reserved,
        url = random_string(100)
    )

    with pytest.raises(KeyError):
        access.update(testhook)
    
def test_crud_bad_delete(session):
    access = webhook.WebhookAccess(session)
    testhook = webhook.Webhook(
        hooktype = webhook.HookType.slot_reserved,
        url = random_string(100)
    )

    with pytest.raises(KeyError):
        access.delete(testhook)
