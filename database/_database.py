from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database_interface import DatabaseInterface
from database.managers import ProductManager, CategoryManager
from database.models import BaseModel


class Database(DatabaseInterface):
    def __init__(self, database_url: str):
        self.__engine = create_engine(database_url, connect_args={"check_same_thread": False})
        BaseModel.metadata.create_all(self.__engine)
        self.__category_manager = CategoryManager(self)
        self.__product_manager = ProductManager(self)

    def get_session(self) -> Session:
        session = Session(self.__engine, autoflush=False)
        return session

    def get_category_manager(self) -> CategoryManager:
        return self.__category_manager

    def get_product_manager(self) -> ProductManager:
        return self.__product_manager
