from uuid import uuid4

import pytest

from app.database_interface.exceptions import NotFound
from app.models import Product
from app.tests import FakeDatabase, FakeProductManager


def test_get_product_by_uuid(fake_database: FakeDatabase, product_manager: FakeProductManager):
    product_uuid = uuid4()
    category_uuid = uuid4()
    fake_database.storage = {
        "categories": {
            category_uuid: {
                "title": "title"
            }
        },
        "products": {
            product_uuid: {
                "title": "title",
                "description": "description",
                "cost": 1,
                "category": category_uuid
            }
        }
    }
    product: Product = product_manager.get_by_uuid(uuid=product_uuid)
    assert product.title == "title"
    assert product.description == "description"
    assert product.cost == 1
    assert product.category.title == "title"


def test_delete_product_by_uuid(fake_database: FakeDatabase, product_manager: FakeProductManager):
    product_uuid = uuid4()
    category_uuid = uuid4()
    fake_database.storage = {
        "categories": {
            category_uuid: {
                "title": "title"
            }
        },
        "products": {
            product_uuid: {
                "title": "title",
                "description": "description",
                "cost": 1,
                "category": category_uuid
            }
        }
    }

    product_manager.get_by_uuid(uuid=product_uuid)
    product_manager.delete_by_uuid(uuid=product_uuid)
    with pytest.raises(NotFound):
        product_manager.get_by_uuid(uuid=product_uuid)


def test_create_product(fake_database: FakeDatabase, product_manager: FakeProductManager):
    category_uuid = uuid4()
    fake_database.storage = {
        "categories": {
            category_uuid: {
                "title": "title"
            }
        },
        "products": {}
    }
    product_uuid = product_manager.create(
        title="title",
        description="description",
        cost=1,
        category=category_uuid
    )
    product: Product = product_manager.get_by_uuid(uuid=product_uuid)
    assert product.title == "title"
    assert product.description == "description"
    assert product.cost == 1
    assert product.category.title == "title"


def test_update_product(fake_database: FakeDatabase, product_manager: FakeProductManager):
    product_uuid = uuid4()
    category1_uuid = uuid4()
    category2_uuid = uuid4()
    fake_database.storage = {
        "categories": {
            category1_uuid: {
                "title": "title 1"
            },
            category2_uuid: {
                "title": "title 2"
            }
        },
        "products": {
            product_uuid: {
                "title": "title",
                "description": "description",
                "cost": 1,
                "category": category1_uuid
            }
        }
    }
    product: Product = product_manager.get_by_uuid(uuid=product_uuid)
    assert product.title == "title"
    assert product.description == "description"
    assert product.cost == 1
    assert product.category.title == "title 1"

    product_manager.update_by_uuid(
        uuid=product_uuid,
        title="updated title",
        description="updated description",
        cost=2,
        category=category2_uuid
    )

    product: Product = product_manager.get_by_uuid(uuid=product_uuid)
    assert product.title == "updated title"
    assert product.description == "updated description"
    assert product.cost == 2
    assert product.category.title == "title 2"


def test_filter_products(fake_database: FakeDatabase, product_manager: FakeProductManager):
    category1_uuid = uuid4()
    category2_uuid = uuid4()
    fake_database.storage = {
        "categories": {
            category1_uuid: {
                "title": "title 1"
            },
            category2_uuid: {
                "title": "title 2"
            }
        },
        "products": {
            uuid4(): {
                "title": "title 1",
                "description": "description 1",
                "cost": 100,
                "category": category1_uuid
            },
            uuid4(): {
                "title": "title 2",
                "description": "description 2",
                "cost": 200,
                "category": category1_uuid
            },
            uuid4(): {
                "title": "title 3",
                "description": "description 3",
                "cost": 300,
                "category": category2_uuid
            }
        }
    }
    assert len(product_manager.filter(offset=0, limit=2)) == 2
    assert len(product_manager.filter(offset=2, limit=2)) == 1

    assert len(product_manager.filter(title__contains="title", offset=0, limit=3)) == 3
    assert len(product_manager.filter(title__contains="1", offset=0, limit=3)) == 1

    assert len(product_manager.filter(description__contains="description", offset=0, limit=3)) == 3
    assert len(product_manager.filter(description__contains="1", offset=0, limit=3)) == 1

    assert len(product_manager.filter(cost=100, offset=0, limit=3)) == 1
    assert len(product_manager.filter(cost__greater_than_or_equal_to=100, offset=0, limit=3)) == 3
    assert len(product_manager.filter(cost__greater_than=100, offset=0, limit=3)) == 2
    assert len(product_manager.filter(cost__lower_than_or_equal_to=300, offset=0, limit=3)) == 3
    assert len(product_manager.filter(cost__lower_than=300, offset=0, limit=3)) == 2

    assert len(product_manager.filter(category__in=[category1_uuid], offset=0, limit=3)) == 2
