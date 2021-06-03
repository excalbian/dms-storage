""" All database modules used for the application
    Uses flask-sqlalchemy, flask-marshmallow for ORM and json schema
"""
from pydantic import BaseModel as PydanticBaseModel
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# List for alembic to find our modules
from os.path import dirname, basename, isfile, join
import glob

from pydantic.decorator import validate_arguments
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

class PydanticBase(PydanticBaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True

@as_declarative()
class DbBase:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()