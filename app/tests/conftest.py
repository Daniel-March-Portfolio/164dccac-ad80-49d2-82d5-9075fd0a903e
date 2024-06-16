import pytest

from app.tests.fake_database import FakeDatabase


@pytest.fixture
def fake_database() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture
def product_manager(fake_database):
    return fake_database.get_product_manager()


@pytest.fixture
def category_manager(fake_database):
    return fake_database.get_category_manager()
