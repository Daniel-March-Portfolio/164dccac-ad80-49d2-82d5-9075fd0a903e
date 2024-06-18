from fastapi.testclient import TestClient

from api import API
from app.tests.conftest import *


@pytest.fixture
def api(app):
    return API(app)


@pytest.fixture
def client(api):
    return TestClient(api)
