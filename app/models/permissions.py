from datetime import datetime
from enum import unique
from app.appdef import db

class Permissions(db.Model):
    """ Permissions DB Model
        Permissions table for users that have beyond-base permissions. All
        users should have the ability to login and reserve storage when available (unless banned).
        This table is just for users that need admin, reportability, overrides, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    can_report = db.Column(db.Boolean, default=False)
    can_configure = db.Column(db.Boolean, default=False)
    can_ban = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)