from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from app.database_interface.exceptions import NotFound, Conflict
from database import Database
from database.managers import CategoryManager
from database.models import CategoryDB


def test_get_category_manager(database: Database, category_manager: CategoryManager):
    assert database.get_category_manager() is category_manager


def test_get_by_uuid(category_manager: CategoryManager, db_session: Session):
    database_category = CategoryDB(title="test")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    logic_category = category_manager.get_by_uuid(uuid=database_category.uuid)
    assert logic_category.title == database_category.title


def test_get_by_uuid_not_found(category_manager: CategoryManager):
    with pytest.raises(NotFound):
        category_manager.get_by_uuid(uuid=uuid4())


def test_filter(category_manager: CategoryManager, db_session: Session):
    database_categories = [
        CategoryDB(title="title 1"),
        CategoryDB(title="title 2"),
        CategoryDB(title="title 3")
    ]
    db_session.add_all(database_categories)
    db_session.commit()

    assert len(category_manager.filter(offset=0, limit=2)) == 2
    assert len(category_manager.filter(offset=2, limit=2)) == 1

    assert len(category_manager.filter(title__contains="title", offset=0, limit=3)) == 3
    assert len(category_manager.filter(title__contains="1", offset=0, limit=3)) == 1


def test_create(category_manager: CategoryManager, db_session: Session):
    category_uuid = category_manager.create(title="title")
    all_categories = category_manager.filter(offset=0, limit=1)
    assert category_uuid == all_categories[0]


def test_create_with_conflict(category_manager: CategoryManager, db_session: Session):
    category_manager.create(title="title")

    with pytest.raises(Conflict):
        category_manager.create(title="title")


def test_update_by_uuid(category_manager: CategoryManager, db_session: Session):
    database_category = CategoryDB(title="title")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    logic_updated_category = category_manager.update_by_uuid(
        uuid=database_category.uuid,
        title="updated title",
    )
    assert logic_updated_category.title == "updated title"

    database_category = category_manager._get_database_model_by_uuid(uuid=database_category.uuid)
    assert database_category.title == "updated title"


def test_update_with_conflict(category_manager: CategoryManager, db_session: Session):
    category_manager.create(title="conflict title")
    category_uuid = category_manager.create(title="title")

    with pytest.raises(Conflict):
        category_manager.update_by_uuid(
            uuid=category_uuid,
            title="conflict title",
        )


def test_delete_by_uuid(category_manager: CategoryManager, db_session: Session):
    database_category = CategoryDB(title="title")
    db_session.add(database_category)
    db_session.commit()
    db_session.refresh(database_category)

    category_manager.get_by_uuid(uuid=database_category.uuid)
    category_manager.delete_by_uuid(uuid=database_category.uuid)
    with pytest.raises(NotFound):
        category_manager.get_by_uuid(uuid=database_category.uuid)


def test_delete_by_uuid_not_found(category_manager: CategoryManager):
    with pytest.raises(NotFound):
        category_manager.delete_by_uuid(uuid=uuid4())
