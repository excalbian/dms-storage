from datetime import datetime
from app.appdef import db, app
from flask_marshmallow import Marshmallow
from .user import User, UserSchema

import enum

ma = Marshmallow(app)

class AuditType(str, enum.Enum):
    """ All types of actions logged in the audit table """
    login = 'login'
    slotreserved = 'slotreserved'
    slotreleased = 'slotreleased'
    userupdated = 'userupdated'
    reportrun = 'reportrun'
    slotupdated = 'slotupdated'

class AuditLog(db.Model):
    """ Represents an audit entry in the database. Used for all
        actions that should be auditable """
    id = db.Column(db.Integer, primary_key=True)
    logtime = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Enum(AuditType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    data = db.Column(db.JSON)
    user = db.relationship(User.__name__)

class AuditLogSchema(ma.SQLAlchemySchema):
    """ Used during JSON conversion of the database model object """
    class Meta:
        model = AuditLog
    
    id = ma.auto_field(dump_only=True)
    logtime = ma.auto_field(dump_only=True)
    type = ma.auto_field()
    message = ma.auto_field()
    data = ma.auto_field()
    user = ma.Nested(UserSchema, only=['id','username'] )