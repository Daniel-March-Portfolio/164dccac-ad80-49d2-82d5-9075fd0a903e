from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from database.models.__base import BaseModel


class CategoryDB(BaseModel):
    __tablename__ = "category"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(unique=True)
