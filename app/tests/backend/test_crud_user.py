import app.backend.app.data.user as user
from .fixtures import *
from app.tests.utils.randoms import random_string

def test_crud_create(session):
    useraccess = user.UserAccess(session)
    testuser = user.User(
            username = "testuser",
            displayname = "test user",
            email = "test@example.com",
            phone="123-456-7890",

        )
    result = useraccess.create_user(testuser)

    assert testuser.id == -1
    assert result.id == 1
    assert result.displayname == "test user"
    assert result.username == "testuser"
    assert result.can_ban == False
    assert result.can_configure == False
    assert result.can_report == False
    assert result.email == "test@example.com"
    assert result.is_active == True
    assert result.is_admin == False
    assert result.is_banned == False

def test_crud_get(session):
    useraccess = user.UserAccess(session)
    testuser = useraccess.create_user(user.User(
            username = "testuser",
            displayname = "test user",
            email = "test@example.com",
            phone="123-456-7890",

        ))
    result = useraccess.get_user_by_username('testuser')
    assert testuser == result