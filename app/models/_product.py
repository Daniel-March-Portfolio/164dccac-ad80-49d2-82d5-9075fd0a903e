from dataclasses import dataclass

from app.models.__type import LogicModelType
from app.models._category import Category


@dataclass
class Product(LogicModelType):
    title: str
    description: str
    cost: int
    category: Category
