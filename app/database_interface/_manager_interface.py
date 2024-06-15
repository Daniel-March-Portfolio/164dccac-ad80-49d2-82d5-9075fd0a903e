from abc import ABC, abstractmethod
from uuid import UUID

from app.models import LogicModelType


class ManagerInterface(ABC):
    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> LogicModelType: ...

    @abstractmethod
    def filter(self, offset: int, limit: int, **kwargs) -> list[UUID]:
        """
        Available filtering parameters:
        <field>__lower_than
        <field>__lower_than_or_equal_to
        <field>__greater_than
        <field>__greater_than_or_equal_to
        <field>__not_in
        <field>__in
        <field>__not_equal
        <field>__contains
        """
        ...

    @abstractmethod
    def create(self, **values) -> UUID: ...

    @abstractmethod
    def update_by_uuid(self, uuid: UUID, **new_values) -> LogicModelType: ...

    @abstractmethod
    def delete_by_uuid(self, uuid: UUID) -> None: ...
