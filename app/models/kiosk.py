from datetime import datetime
from app.appdef import db


class Kiosk(db.Model):
    """ Kiosk DB Model
        Meant to represent an address or machine name of a kiosk, to 
        automatically put it in a kiosk mode. The printer name will
        be used to connect and print out tags when necessary.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    printer_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)