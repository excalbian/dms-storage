from app.appdef import db

class Configuration(db.Model):
    """ Configuration DB class
        Represents simple key/value configuration entries for the application. Meant
        to be read once and cached.
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(25), index=True, unique=True)
    value = db.Column(db.Text)
