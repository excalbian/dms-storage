from datetime import datetime
from app.appdef import db, app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class StorageType(db.Model):
    """ StorageType DB Model
        Represents a type of storage - e.g. flex area vertical, flex area shelf, 
        warehouse large shelf, ikea tub, etc. Should have a name and a location, but is 
        not a reservable space - that is a storage slot.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=True)
    valid_days = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class StorageTypeSchema(ma.SQLAlchemySchema):
    """ StorageTypeSchema
        Used for serialization
    """
    class Meta:
        model = StorageType
    
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    location = ma.auto_field()
    valid_days = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)