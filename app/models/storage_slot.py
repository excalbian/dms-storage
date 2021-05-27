from sqlalchemy import DateTime
from .storage_type import StorageType, StorageTypeSchema
from datetime import datetime
from app.appdef import db, app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class StorageSlot(db.Model):
    """ Storage Slot DB Model
        Represents a single reserveable place for storage.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    storage_type_id = db.Column(db.Integer, db.ForeignKey('storage_type.id'))
    created_at = db.Column(DateTime, default=datetime.now)
    updated_at = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    storage_type = db.relationship(StorageType.__name__)

class StorageSlotSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StorageSlot
    
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    storage_type = ma.Nested(StorageTypeSchema)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)