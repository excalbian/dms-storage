""" All database modules used for the application
    Uses flask-sqlalchemy, flask-marshmallow for ORM and json schema
"""
from pydantic import BaseModel as PydanticBaseModel

# List for alembic to find our modules
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

class PydanticBase(PydanticBaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True