import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import Database
from database.models import BaseModel

DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def database(engine):
    return Database(DATABASE_URL)


@pytest.fixture(scope="function")
def product_manager(database):
    return database.get_product_manager()


@pytest.fixture(scope="function")
def category_manager(database):
    return database.get_category_manager()


@pytest.fixture(scope="function")
def engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="function")
def tables(engine):
    BaseModel.metadata.create_all(bind=engine)
    yield
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine, tables):
    BaseModel.metadata.create_all(engine)
    session = Session(engine, autoflush=False)
    return session
