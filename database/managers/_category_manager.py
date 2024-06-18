from typing import Sequence
from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.exc import OperationalError, IntegrityError

from app.database_interface.exceptions import NotFound, Conflict
from app.models import Category
from database.managers.__base import BaseManager
from database.models import CategoryDB


class CategoryManager(BaseManager):
    def get_by_uuid(self, uuid: UUID) -> Category:
        result = self._get_database_model_by_uuid(uuid)
        logic_model = self.__convert_database_model_to_logic_model(result)
        return logic_model

    def _get_database_model_by_uuid(self, uuid: UUID) -> CategoryDB:
        stmt = (
            select(CategoryDB)
            .where(CategoryDB.uuid == uuid)
        )

        session = self._database.get_session()
        database_model = session.execute(stmt).scalars().first()

        if database_model is None:
            raise NotFound(f"Category with uuid {uuid} not found")
        session.close()
        return database_model

    @staticmethod
    def __convert_database_model_to_logic_model(database_model: CategoryDB) -> Category:
        return Category(
            title=database_model.title,
        )

    def filter(self, offset: int, limit: int, **kwargs) -> list[UUID]:
        stmt = (
            select(CategoryDB.uuid)
            .where(*self._create_query_filter(database_model_type=CategoryDB, **kwargs))
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
            insert(CategoryDB)
            .values(**values)
            .returning(CategoryDB.uuid)
        )

        session = self._database.get_session()
        try:
            result = session.execute(stmt)
        except IntegrityError:
            session.close()
            raise Conflict()
        uuid = result.scalar_one()
        session.commit()

        session.close()
        return uuid

    def update_by_uuid(self, uuid: UUID, **new_values) -> Category:
        stmt = (
            update(CategoryDB)
            .values(**new_values)
            .where(CategoryDB.uuid == uuid)
        )

        session = self._database.get_session()
        try:
            session.execute(stmt)
        except IntegrityError:
            raise Conflict()
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
