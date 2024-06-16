from abc import ABC
from copy import copy
from uuid import UUID, uuid4

from app.database_interface import DatabaseInterface, ManagerInterface
from app.database_interface.exceptions import NotFound
from app.models import LogicModelType, Product, Category


class FakeManager(ManagerInterface, ABC):
    def __init__(self, database: "FakeDatabase", table: str):
        self._database = database
        self._table = table

    def filter(self, offset: int, limit: int, **kwargs) -> list[UUID]:
        storage = self._database.get_session()[self._table]
        selected = []
        for uuid, logic_model_data in storage.items():
            if offset > 0:
                offset -= 1
                continue
            if limit <= 0:
                break
            limit -= 1
            if self._filter_check(logic_model_data, **kwargs):
                selected.append(uuid)
        return selected

    def create(self, **values) -> UUID:
        storage = self._database.get_session()[self._table]
        uuid = uuid4()
        storage[uuid] = values
        return uuid

    def update_by_uuid(self, uuid: UUID, **new_values) -> LogicModelType:
        storage = self._database.get_session()[self._table]
        logic_model = storage[uuid]
        for field, value in new_values.items():
            logic_model[field] = value
        return self.get_by_uuid(uuid)

    def delete_by_uuid(self, uuid: UUID) -> None:
        self.get_by_uuid(uuid)
        storage = self._database.get_session()[self._table]
        del storage[uuid]

    @staticmethod
    def _filter_check(logic_model_data: dict, **kwargs) -> bool:
        for key, value in kwargs.items():
            if key[-12:] == "__lower_than":
                if not logic_model_data[key[:-12]] < value:
                    return False
            elif key[-24:] == "__lower_than_or_equal_to":
                if not logic_model_data[key[:-24]] <= value:
                    return False
            elif key[-14:] == "__greater_than":
                if not logic_model_data[key[:-14]] > value:
                    return False
            elif key[-26:] == "__greater_than_or_equal_to":
                if not logic_model_data[key[:-26]] >= value:
                    return False
            elif key[-8:] == "__not_in":
                if logic_model_data[key[:-8]] in value:
                    return False
            elif key[-4:] == "__in":
                if logic_model_data[key[:-4]] not in value:
                    return False
            elif key[-11:] == "__not_equal":
                if not logic_model_data[key[:-11]] != value:
                    return False
            elif key[-10:] == "__contains":
                if value not in logic_model_data[key[:-10]]:
                    return False
            else:
                if not logic_model_data[key] == value:
                    return False
        return True


class FakeProductManager(FakeManager):

    def get_by_uuid(self, uuid: UUID) -> Product:
        storage = self._database.get_session()[self._table]
        if uuid not in storage:
            raise NotFound(f"Product with uuid {uuid} not found")
        logic_model_data = copy(storage[uuid])
        category_manager = self._database.get_category_manager()
        logic_model_data["category"] = category_manager.get_by_uuid(logic_model_data["category"])
        logic_model = Product(**logic_model_data)
        return logic_model


class FakeCategoryManager(FakeManager):

    def get_by_uuid(self, uuid: UUID) -> Category:
        storage = self._database.get_session()[self._table]
        if uuid not in storage:
            raise NotFound(f"Category with uuid {uuid} not found")
        logic_model_data = copy(storage[uuid])
        logic_model = Category(**logic_model_data)
        return logic_model


class FakeDatabase(DatabaseInterface):
    def __init__(self):
        self.storage = {
            "products": {},
            "categories": {},
        }
        self._product_manager = FakeProductManager(self, "products")
        self._category_manager = FakeCategoryManager(self, "categories")

    def get_category_manager(self):
        return self._category_manager

    def get_product_manager(self):
        return self._product_manager

    def get_session(self) -> dict:
        return self.storage
