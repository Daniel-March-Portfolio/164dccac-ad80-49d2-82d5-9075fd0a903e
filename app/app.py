from uuid import UUID

from app import exceptions as app_exceptions
from app._interface import AppInterface
from app.database_interface import DatabaseInterface
from app.database_interface import exceptions as database_exceptions
from app.models import Product, Category


class App(AppInterface):
    LIMIT = 10  # Todo move to config file

    def __init__(self, database: DatabaseInterface):
        self.__database = database

    def get_product(self, uuid: UUID) -> Product:
        product_manager = self.__database.get_product_manager()
        try:
            product = product_manager.get_by_uuid(uuid)
        except database_exceptions.NotFound:
            raise app_exceptions.ProductNotFound(f"Product with uuid {uuid} not found")
        return product

    def filter_products(self, page: int, **kwargs) -> list[UUID]:
        for key, value in list(kwargs.items()):
            if key.startswith("category_uuid"):
                kwargs["category" + key[13:]] = value
                del kwargs[key]
        product_manager = self.__database.get_product_manager()
        product = product_manager.filter(offset=page * self.LIMIT, limit=self.LIMIT, **kwargs)
        return product

    def create_product(self, title: str, description: str, cost: int, category_uuid: UUID) -> UUID:
        self.get_category(uuid=category_uuid)
        product_manager = self.__database.get_product_manager()
        product_uuid = product_manager.create(
            title=title, description=description, cost=cost, category=category_uuid
        )
        return product_uuid

    def update_product_by_uuid(self, uuid: UUID, **new_values) -> Product:
        self.get_product(uuid=uuid)
        if "category_uuid" in list(new_values.keys()):
            new_values["category"] = new_values["category_uuid"]
            del new_values["category_uuid"]
            self.get_category(uuid=new_values["category"])
        product_manager = self.__database.get_product_manager()
        updated_product = product_manager.update_by_uuid(uuid=uuid, **new_values)
        return updated_product

    def delete_product_by_uuid(self, uuid: UUID) -> None:
        product_manager = self.__database.get_product_manager()
        self.get_product(uuid=uuid)
        product_manager.delete_by_uuid(uuid=uuid)

    def filter_categories(self, page: int, **kwargs) -> list[UUID]:
        category_manager = self.__database.get_category_manager()
        categories = category_manager.filter(offset=page * self.LIMIT, limit=self.LIMIT, **kwargs)
        return categories

    def get_category(self, uuid: UUID) -> Category:
        category_manager = self.__database.get_category_manager()
        try:
            category = category_manager.get_by_uuid(uuid)
        except database_exceptions.NotFound:
            raise app_exceptions.CategoryNotFound(f"Category with uuid {uuid} not found")
        return category

    def create_category(self, title: str) -> UUID:
        category_manager = self.__database.get_category_manager()
        category_uuid = category_manager.create(title=title)
        return category_uuid

    def update_category_by_uuid(self, uuid: UUID, **new_values) -> Category:
        self.get_category(uuid=uuid)
        category_manager = self.__database.get_category_manager()
        updated_category = category_manager.update_by_uuid(uuid=uuid, **new_values)
        return updated_category

    def delete_category_by_uuid(self, uuid: UUID) -> None:
        self.get_category(uuid=uuid)
        category_manager = self.__database.get_category_manager()
        category_manager.delete_by_uuid(uuid=uuid)
