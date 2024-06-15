from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models.__base import BaseModel
from database.models._category import CategoryDB


class ProductDB(BaseModel):
    __tablename__ = "product"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    description: Mapped[str]
    cost: Mapped[int]
    category: Mapped[CategoryDB] = mapped_column(ForeignKey(CategoryDB.uuid))
