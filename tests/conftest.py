import pytest
from sanic import Sanic
from tinydb import TinyDB

from server import create_app


@pytest.fixture
def app() -> Sanic:
    return create_app()


@pytest.fixture(scope="session")
def db() -> TinyDB:
    database = TinyDB("db_test.json")
    yield database
    database.truncate()
