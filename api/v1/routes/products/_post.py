from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from api.v1.utils import get_app_from_request
from app.exceptions import CategoryNotFound


class ProductPostSchema(BaseModel):
    title: str
    description: str
    cost: int
    category_uuid: UUID


async def products_post(request: Request, data: ProductPostSchema):
    app = get_app_from_request(request)

    try:
        product_uuid = app.create_product(**data.model_dump())
    except CategoryNotFound:
        return Response(status_code=404, content="Category not found")

    return Response(content=str(product_uuid), status_code=201)
