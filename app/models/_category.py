from dataclasses import dataclass

from app.models.__type import LogicModelType


@dataclass
class Category(LogicModelType):
    title: str
