from typing import Sequence
from uuid import UUID

from sqlalchemy import select, insert, update

from app.database_interface.exceptions import NotFound
from app.models import Product
from database.managers.__base import BaseManager
from database.models import ProductDB


class ProductManager(BaseManager):
    def get_by_uuid(self, uuid: UUID) -> Product:
        result = self._get_database_model_by_uuid(uuid)
        logic_model = self.__convert_database_model_to_logic_model(result)
        return logic_model

    def _get_database_model_by_uuid(self, uuid: UUID) -> ProductDB:
        stmt = (
            select(ProductDB)
            .where(ProductDB.uuid == uuid)
        )

        session = self._database.get_session()
        database_model = session.execute(stmt).scalars().first()

        if database_model is None:
            raise NotFound(f"Product with uuid {uuid} not found")
        session.close()
        return database_model

    def __convert_database_model_to_logic_model(self, database_model: ProductDB) -> Product:
        category_manager = self._database.get_category_manager()
        logic_category_model = category_manager.get_by_uuid(database_model.category)
        return Product(
            title=database_model.title,
            description=database_model.description,
            cost=database_model.cost,
            category=logic_category_model,
        )

    def filter(self, offset: int, limit: int, **kwargs) -> list[UUID]:
        stmt = (
            select(ProductDB.uuid)
            .where(*self._create_query_filter(database_model_type=ProductDB, **kwargs))
            .offset(offset)
            .limit(limit)
        )

        session = self._database.get_session()
        sequence_of_uuids: Sequence[UUID] = session.execute(stmt).scalars().all()
        list_of_uuids = list(sequence_of_uuids)
        session.close()
        return list_of_uuids

    def create(self, **values) -> UUID:
        stmt = (
            insert(ProductDB)
            .values(**values)
            .returning(ProductDB.uuid)
        )

        session = self._database.get_session()
        result = session.execute(stmt)
        uuid = result.scalar_one()
        session.commit()

        session.close()
        return uuid

    def update_by_uuid(self, uuid: UUID, **new_values) -> Product:
        stmt = (
            update(ProductDB)
            .values(**new_values)
            .where(ProductDB.uuid == uuid)
        )

        session = self._database.get_session()
        session.execute(stmt)
        session.commit()

        logic_model = self.get_by_uuid(uuid)
        session.close()
        return logic_model

    def delete_by_uuid(self, uuid: UUID) -> None:
        database_model = self._get_database_model_by_uuid(uuid)

        session = self._database.get_session()
        session.delete(database_model)
        session.commit()
        session.close()
