from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.database_interface._manager_interface import ManagerInterface


class DatabaseInterface(ABC):
    @abstractmethod
    def get_category_manager(self) -> ManagerInterface: ...

    @abstractmethod
    def get_product_manager(self) -> ManagerInterface: ...

    @abstractmethod
    def get_session(self) -> Session: ...
