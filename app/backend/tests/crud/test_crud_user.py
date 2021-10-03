import app.data.user as user
from .fixtures import *
from ..utils.randoms import random_string

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

def test_crud_get_by_username(session):
    useraccess = user.UserAccess(session)
    testuser = useraccess.create_user( user.User(
            username = "testuser",
            displayname = "test user",
            email = "test@example.com",
            phone="123-456-7890",

        ))
    for i in range(0,10):
        useraccess.create_user( user.User(
            username = random_string(15),
            displayname = random_string(30),
            email = random_string(8) + "@example.com"
        ))
    
    result = useraccess.get_user_by_username('testuser')
    assert testuser == result
    
def test_crud_get_users(session):
    useraccess = user.UserAccess(session)
    for i in range(0,99):
        useraccess.create_user( user.User(
            username = random_string(15),
            displayname = random_string(30),
            email = random_string(8) + "@example.com"
        ))
    
    result_1 = useraccess.get_users(skip=0, limit=50)
    result_2 = useraccess.get_users(skip=50, limit=50)

    assert len(result_1) == 50
    assert len(result_2) == 49
    assert result_1[0].username < result_2[0].username
    assert result_1[0] != result_2[0]

def test_crud_update(session):
    useraccess = user.UserAccess(session)
    testuser = user.User(
            username = random_string(15),
            displayname = random_string(30),
            email = random_string(8) + "@example.com"
        )
    createduser = useraccess.create_user(testuser)
    createduser.is_admin = True
    updateduser = useraccess.update_user(createduser)

    assert createduser.id == updateduser.id
    assert updateduser.username == testuser.username
    assert testuser.is_admin == False
    assert updateduser.is_admin == True