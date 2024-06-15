from abc import ABC

from sqlalchemy import ColumnElement

from app.database_interface import DatabaseInterface, ManagerInterface
from database.models import BaseModel


class BaseManager(ManagerInterface, ABC):
    def __init__(self, database: DatabaseInterface):
        self._database = database

    @staticmethod
    def _create_query_filter(database_model_type: type[BaseModel], **kwargs) -> list[ColumnElement]:
        filters = []
        for key, value in kwargs.items():
            if key[-12:] == "__lower_than":
                filters.append(getattr(database_model_type, key[:-12]).__lt__(value))
            elif key[-24:] == "__lower_than_or_equal_to":
                filters.append(getattr(database_model_type, key[:-24]).__le__(value))
            elif key[-14:] == "__greater_than":
                filters.append(getattr(database_model_type, key[:-14]).__gt__(value))
            elif key[-26:] == "__greater_than_or_equal_to":
                filters.append(getattr(database_model_type, key[:-26]).__ge__(value))
            elif key[-8:] == "__not_in":
                filters.append(getattr(database_model_type, key[:-8]).not_in(value))
            elif key[-4:] == "__in":
                filters.append(getattr(database_model_type, key[:-4]).in_(value))
            elif key[-11:] == "__not_equal":
                filters.append(getattr(database_model_type, key[:-11]).__ne__(value))
            elif key[-10:] == "__contains":
                a = getattr(database_model_type, key[:-10])
                filters.append(a.contains(value))
            else:
                filters.append(getattr(database_model_type, key).__eq__(value))
        return filters
