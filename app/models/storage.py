from datetime import datetime
from app.appdef import db, app
from .storage_slot import StorageSlot, StorageSlotSchema
from .user import User, UserSchema
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class Storage(db.Model):
    """ Storage DB Model
        Represents a reservation of a storage slot. Main transactional table for the application
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('storage_slot.id'), nullable=False)
    started = db.Column(db.DateTime, default=datetime.now, nullable=False)
    expiring = db.Column(db.DateTime, nullable=True, index=True)
    ended = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    slot = db.relationship(StorageSlot.__name__)
    user = db.relationship(User.__name__, backref='storage')

class StorageSchema(ma.SQLAlchemySchema):
    """ StorageSchema
        Used for serialization
    """
    class Meta:
        model = Storage
    
    id = ma.auto_field(dump_only=True)
    user = ma.Nested(UserSchema, only=['id','username'] )
    slot = ma.Nested(StorageSlotSchema)
    started = ma.auto_field()
    expiring = ma.auto_field()
    ended = ma.auto_field()
    updated = ma.auto_field()
    