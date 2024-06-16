from uuid import uuid4

import pytest

from app import AppInterface
from app.exceptions import CategoryNotFound, ProductNotFound
from app.tests.fake_database import FakeProductManager, FakeCategoryManager


def test_get_product(app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")
    product_uuid = product_manager.create(
        title="title",
        description="description",
        cost=1,
        category=category_uuid
    )

    product = app.get_product(product_uuid)

    assert product.title == "title"
    assert product.description == "description"
    assert product.cost == 1
    assert product.category.title == "title"


def test_filter_products(app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager):
    category1_uuid = category_manager.create(title="title 1")
    category2_uuid = category_manager.create(title="title 2")
    product_manager.create(
        title="title 1",
        description="description 1",
        cost=100,
        category=category1_uuid
    )
    product_manager.create(
        title="title 2",
        description="description 2",
        cost=200,
        category=category1_uuid
    )
    product_manager.create(
        title="title 3",
        description="description 3",
        cost=300,
        category=category2_uuid
    )

    app.LIMIT = 2

    assert len(app.filter_products(page=0)) == 2
    assert len(app.filter_products(page=1)) == 1

    app.LIMIT = 10
    assert len(app.filter_products(page=0, title__contains="title")) == 3
    assert len(app.filter_products(page=0, title__contains="1")) == 1

    assert len(app.filter_products(page=0, description__contains="description")) == 3
    assert len(app.filter_products(page=0, description__contains="1")) == 1

    assert len(app.filter_products(page=0, cost=100)) == 1
    assert len(app.filter_products(page=0, cost__greater_than_or_equal_to=100)) == 3
    assert len(app.filter_products(page=0, cost__greater_than=100)) == 2
    assert len(app.filter_products(page=0, cost__lower_than_or_equal_to=300)) == 3
    assert len(app.filter_products(page=0, cost__lower_than=300)) == 2

    assert len(app.filter_products(page=0, category_uuid__in=[category1_uuid])) == 2
    assert len(app.filter_products(page=0, category_uuid__not_in=[category1_uuid])) == 1


def test_get_product_not_found(
        app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager
):
    with pytest.raises(ProductNotFound):
        app.get_product(uuid4())


def test_update_product(app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager):
    category1_uuid = category_manager.create(title="title 1")
    category2_uuid = category_manager.create(title="title 2")
    product_uuid = app.create_product(
        title="title",
        description="description",
        cost=1,
        category_uuid=category1_uuid
    )
    new_values = {
        "title": "new title",
        "description": "new description",
        "cost": 2,
        "category": category2_uuid
    }

    updated_product = app.update_product_by_uuid(product_uuid, **new_values)
    product_in_database = product_manager.get_by_uuid(uuid=product_uuid)

    assert updated_product.title == "new title"
    assert updated_product.description == "new description"
    assert updated_product.cost == 2
    assert updated_product.category.title == "title 2"

    assert product_in_database.title == "new title"
    assert product_in_database.description == "new description"
    assert product_in_database.cost == 2
    assert product_in_database.category.title == "title 2"


def test_update_product_not_found(app: AppInterface, product_manager: FakeProductManager):
    with pytest.raises(ProductNotFound):
        app.update_product_by_uuid(uuid4())


def test_update_product_category_not_found(
        app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager
):
    category_uuid = category_manager.create(title="title")
    product_uuid = app.create_product(
        title="title",
        description="description",
        cost=1,
        category_uuid=category_uuid
    )

    with pytest.raises(CategoryNotFound):
        app.update_product_by_uuid(product_uuid, category_uuid=uuid4())


def test_create_product(app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")

    product_uuid = app.create_product(
        title="title",
        description="description",
        cost=1,
        category_uuid=category_uuid
    )

    product = product_manager.get_by_uuid(product_uuid)
    assert product.title == "title"
    assert product.description == "description"
    assert product.cost == 1
    assert product.category.title == "title"


def test_create_product_category_not_found(app: AppInterface, product_manager: FakeProductManager):
    with pytest.raises(CategoryNotFound):
        app.create_product(
            title="title",
            description="description",
            cost=1,
            category_uuid=uuid4()
        )


def test_delete_product(app: AppInterface, product_manager: FakeProductManager, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")
    product_uuid = app.create_product(
        title="title",
        description="description",
        cost=1,
        category_uuid=category_uuid
    )

    app.delete_product_by_uuid(product_uuid)

    with pytest.raises(ProductNotFound):
        app.get_product(product_uuid)


def test_delete_product_not_found(app: AppInterface):
    with pytest.raises(ProductNotFound):
        app.delete_product_by_uuid(uuid4())


def test_get_category(app: AppInterface, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")
    category = app.get_category(uuid=category_uuid)
    assert category.title == "title"


def test_get_category_not_found(app: AppInterface):
    with pytest.raises(CategoryNotFound):
        app.get_category(uuid=uuid4())


def test_create_category(app: AppInterface, category_manager: FakeCategoryManager):
    category_uuid = app.create_category(title="title")
    category = category_manager.get_by_uuid(category_uuid)
    assert category.title == "title"


def test_update_category(app: AppInterface, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")
    new_vales = {
        "title": "new title"
    }

    updated_category = app.update_category_by_uuid(uuid=category_uuid, **new_vales)
    category_in_database = category_manager.get_by_uuid(uuid=category_uuid)

    assert updated_category.title == "new title"
    assert category_in_database.title == "new title"


def test_update_category_not_found(app: AppInterface, category_manager: FakeCategoryManager):
    with pytest.raises(CategoryNotFound):
        app.update_category_by_uuid(uuid4())


def test_delete_category(app: AppInterface, category_manager: FakeCategoryManager):
    category_uuid = category_manager.create(title="title")
    app.delete_category_by_uuid(category_uuid)
    with pytest.raises(CategoryNotFound):
        app.get_category(category_uuid)


def test_delete_category_not_found(app: AppInterface):
    with pytest.raises(CategoryNotFound):
        app.delete_category_by_uuid(uuid4())
