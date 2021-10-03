from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
import app.data.user as user
from app.data import DbBase
import pytest

@pytest.fixture(scope="function")
def engine()->Engine:
    return create_engine("sqlite://")

@pytest.fixture(scope="function")
def tables(engine:Engine):
    DbBase.metadata.create_all(engine)
    yield
    DbBase.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    sm = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield sm
    transaction.rollback()
    connection.close()
