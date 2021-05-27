from datetime import datetime
from app.appdef import db, app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class User(db.Model):
    """ User DB Model
        While not the authoritative source for login, as we'll use OAuth for that,
        this model storage basic information about those users for use with this
        system.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    next_use = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class UserSchema(ma.SQLAlchemySchema):
    """ UserSchema
        Used for serialization of User DB Model
    """
    class Meta:
        model = User
    
    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    next_use = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
