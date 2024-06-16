from abc import ABC, abstractmethod
from typing import overload
from uuid import UUID

from app.models import Product, Category


class AppInterface(ABC):
    @abstractmethod
    def get_product(self, uuid: UUID) -> Product: ...

    @overload
    def filter_products(
            self, page: int, title: str, description: str, cost: int, category_uuid: UUID,
            title__not_in: list[str], title__in: list[str], title__not_equal: list[str], title__contains: str,
            description__not_in: list[str], description__in: list[str], description__not_equal: list[str],
            description__contains: str, cost__lower_than: int, cost__lower_than_or_equal_to: int,
            cost__greater_than: int, cost__greater_than_or_equal_to: int, cost__not_in: list[int], cost__in: list[int],
            cost__not_equal: int, category_uuid__not_in: list[UUID], category_uuid__in: list[UUID],
            category_uuid__not_equal: UUID,
    ) -> list[UUID]:
        ...

    @overload
    def filter_products(self, page: int) -> list[UUID]:
        ...

    @abstractmethod
    def filter_products(self, page: int, **kwargs) -> list[UUID]: ...

    @abstractmethod
    def create_product(self, title: str, description: str, cost: int, category_uuid: UUID) -> UUID: ...

    @overload
    def update_product_by_uuid(
            self, uuid: UUID, title: str, description: str, cost: int, category_uuid: UUID
    ) -> Product:
        ...

    @overload
    def update_product_by_uuid(self, uuid: UUID) -> Product:
        ...

    @abstractmethod
    def update_product_by_uuid(self, uuid: UUID, **new_values) -> Product: ...

    @abstractmethod
    def delete_product_by_uuid(self, uuid: UUID) -> None: ...

    @overload
    def filter_categories(
            self, page: int, title: str, title__not_equal: str, title__contains: str, title__not_in: list[str],
            title__in: list[str]
    ) -> list[UUID]:
        ...

    @overload
    def filter_categories(self, page: int) -> list[UUID]:
        ...

    @abstractmethod
    def filter_categories(self, page: int, **kwargs) -> list[UUID]: ...

    @abstractmethod
    def get_category(self, uuid: UUID) -> Category: ...

    @abstractmethod
    def create_category(self, title: str) -> UUID: ...

    @overload
    def update_category_by_uuid(self, uuid: UUID, title: str) -> Category:
        ...

    @overload
    def update_category_by_uuid(self, uuid: UUID) -> Category:
        ...

    @abstractmethod
    def update_category_by_uuid(self, uuid: UUID, **new_values) -> Category: ...

    @abstractmethod
    def delete_category_by_uuid(self, uuid: UUID) -> None: ...
