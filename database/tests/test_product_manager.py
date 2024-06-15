from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.database_interface.exceptions import NotFound
from database import Database
from database.managers import ProductManager
from database.models import ProductDB, CategoryDB


def test_get_product_manager(database: Database, product_manager: ProductManager):
    assert database.get_product_manager() is product_manager


def test_get_by_uuid(product_manager: ProductManager, db_session: Session):
    database_category = CategoryDB(title="test")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    database_product = ProductDB(
        title="title",
        description="description",
        cost=100,
        category=database_category.uuid,
    )
    db_session.add(database_product)
    db_session.commit()
    db_session.refresh(database_product)

    logic_product = product_manager.get_by_uuid(uuid=database_product.uuid)
    assert logic_product.title == database_product.title
    assert logic_product.description == database_product.description
    assert logic_product.cost == database_product.cost
    assert logic_product.category.title == database_category.title


def test_get_by_uuid_not_found(product_manager: ProductManager):
    with pytest.raises(NotFound):
        product_manager.get_by_uuid(uuid=uuid4())


def test_filter(product_manager: ProductManager, db_session: Session):
    database_category = CategoryDB(title="test")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    database_products = [
        ProductDB(
            title="title 1",
            description="first description",
            cost=100,
            category=database_category.uuid,
        ),
        ProductDB(
            title="title 2",
            description="second description",
            cost=200,
            category=database_category.uuid,
        ),
        ProductDB(
            title="title 3",
            description="third description",
            cost=300,
            category=database_category.uuid,
        )
    ]
    db_session.add_all(database_products)
    db_session.commit()

    assert len(product_manager.filter(offset=0, limit=2)) == 2
    assert len(product_manager.filter(offset=2, limit=2)) == 1

    assert len(product_manager.filter(title__contains="title", offset=0, limit=3)) == 3
    assert len(product_manager.filter(title__contains="1", offset=0, limit=3)) == 1

    assert len(product_manager.filter(description__contains="description", offset=0, limit=3)) == 3
    assert len(product_manager.filter(description__contains="first", offset=0, limit=3)) == 1

    assert len(product_manager.filter(cost=100, offset=0, limit=3)) == 1
    assert len(product_manager.filter(cost__greater_than_or_equal_to=100, offset=0, limit=3)) == 3
    assert len(product_manager.filter(cost__greater_than=100, offset=0, limit=3)) == 2
    assert len(product_manager.filter(cost__lower_than_or_equal_to=300, offset=0, limit=3)) == 3
    assert len(product_manager.filter(cost__lower_than=300, offset=0, limit=3)) == 2


def test_create(product_manager: ProductManager, db_session: Session):
    database_category = CategoryDB(title="test")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    product_uuid = product_manager.create(
        title="title",
        description="description",
        cost=100,
        category=database_category.uuid,
    )
    all_products = product_manager.filter(offset=0, limit=1)
    assert product_uuid == all_products[0]


def test_update_by_uuid(product_manager: ProductManager, db_session: Session):
    database_category_1 = CategoryDB(title="test 1")
    database_category_2 = CategoryDB(title="test 2")
    db_session.add_all([database_category_1, database_category_2])
    db_session.commit()
    db_session.refresh(database_category_1)
    db_session.refresh(database_category_2)

    database_product = ProductDB(
        title="title",
        description="description",
        cost=100,
        category=database_category_1.uuid,
    )
    db_session.add(database_product)
    db_session.commit()
    db_session.refresh(database_product)

    logic_updated_product = product_manager.update_by_uuid(
        uuid=database_product.uuid,
        title="updated title",
        description="updated description",
        cost=200,
        category=database_category_2.uuid
    )
    assert logic_updated_product.title == "updated title"
    assert logic_updated_product.description == "updated description"
    assert logic_updated_product.cost == 200
    assert logic_updated_product.category.title == database_category_2.title

    database_product = product_manager._get_database_model_by_uuid(uuid=database_product.uuid)
    assert database_product.title == "updated title"
    assert database_product.description == "updated description"
    assert database_product.cost == 200
    assert database_product.category == database_category_2.uuid


def test_delete_by_uuid(product_manager: ProductManager, db_session: Session):
    database_category = CategoryDB(title="test")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)
    database_product = ProductDB(
        title="title",
        description="description",
        cost=100,
        category=database_category.uuid,
    )
    db_session.add(database_product)
    db_session.commit()
    db_session.refresh(database_product)

    product_manager.get_by_uuid(uuid=database_product.uuid)
    product_manager.delete_by_uuid(uuid=database_product.uuid)
    with pytest.raises(NotFound):
        product_manager.get_by_uuid(uuid=database_product.uuid)


def test_delete_by_uuid_not_found(product_manager: ProductManager):
    with pytest.raises(NotFound):
        product_manager.delete_by_uuid(uuid=uuid4())
