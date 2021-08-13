
import app.data.auditlog as auditlog
import datetime
from .fixtures import *
from app.tests.utils.randoms import random_string

def test_crud_create(session):
    useraccess = user.UserAccess(session)
    testuser = useraccess.create_user( 
        user.User(
            username = "testuser",
            email = "test@example.com"
        )
    )
    access = auditlog.AuditLogAccess(session)
    tm = datetime.datetime(2020,1,1,0,0,0)
    new_auditlog = auditlog.AuditLog(
        user = testuser,
        logtime = tm,
        logtype = auditlog.AuditType.login,
        message = "TEST"
    )
    created = access.create(new_auditlog)

    assert created.logtime != tm    # Should take the write time, not the time passed in
    assert created.user.id == testuser.id
    assert created.logtype == auditlog.AuditType.login
    assert created.message == "TEST"

def test_crud_byuser(session):
    useraccess = user.UserAccess(session)
    access = auditlog.AuditLogAccess(session)

    data = [
        (useraccess.create_user( 
            user.User(
                username = random_string(8),
                email = random_string(8) + "@example.com" )
        ),[ ]),
        (useraccess.create_user( 
            user.User(
                username = random_string(8),
                email = random_string(8) + "@example.com" )
        ),[ ])
    ]


    for u, log in data:
        log.append( access.create(auditlog.AuditLog(
            user = u,
            logtype = auditlog.AuditType.reportrun,
            message = random_string(20)
        )))
        log.append( access.create(auditlog.AuditLog(
            user = u,
            logtype = auditlog.AuditType.login,
            message = random_string(20)
        )))

    u1_logs = access.get_by_user(data[0][0]) #first tuple, first field = user

    assert len(u1_logs) == 2
    assert u1_logs[0].logtime > u1_logs[1].logtime # should give newest log first
    assert u1_logs[0].user.id == data[0][0].id
    assert u1_logs[1].user.id == data[0][0].id


def test_paging(session):
    useraccess = user.UserAccess(session)
    access = auditlog.AuditLogAccess(session)

    testuser = useraccess.create_user( 
            user.User(
                username = random_string(8),
                email = random_string(8) + "@example.com" )
        )

    for i in range(1,99):
        access.create(auditlog.AuditLog(
            user = testuser,
            logtype = auditlog.AuditType.reportrun,
            message = random_string(20)
        ))

    all_logs = access.get_by_user(testuser)

    logs_1 = access.get_by_user(testuser,0,50)
    logs_2 = access.get_by_user(testuser,50,50)

    assert len(all_logs) == 98
    assert len(logs_1) == 50
    assert len(logs_2) == 48
    assert logs_1[0].user.id == testuser.id
    assert all_logs[0].logtime > all_logs[97].logtime

def test_by_date(session):
    useraccess = user.UserAccess(session)
    access = auditlog.AuditLogAccess(session)

    #clear audit log
    with session() as db:
         db.query(auditlog.DbAuditLog).delete()
         db.commit()
    
    testuser = useraccess.create_user( 
            user.User(
                username = random_string(8),
                email = random_string(8) + "@example.com" )
        )

    with session() as db:
        for i in range(0,100):
        
            db.add(auditlog.DbAuditLog( 
                    logtype = auditlog.AuditType.slotupdated,
                    logtime = datetime.datetime(2020,1,1,0,0,0) + datetime.timedelta(days=i),
                    user_id = testuser.id,
                    message = random_string(20),
                    data = "" ))
        db.commit()

    all_logs_1 = access.get_by_date(date_from=datetime.datetime(2020,1,21,0,0,0), date_to=datetime.datetime.max, skip=0, limit=50)
    all_logs_2 = access.get_by_date(date_from=datetime.datetime(2020,1,21,0,0,0), date_to=datetime.datetime.max, skip=50, limit=50)

    assert len(all_logs_1) == 50
    assert len(all_logs_2) == 30
    assert all_logs_1[0].user.id == testuser.id
    assert all_logs_1[0].logtime > all_logs_1[49].logtime