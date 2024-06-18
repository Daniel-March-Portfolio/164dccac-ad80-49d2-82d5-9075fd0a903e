from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from api.v1.utils import get_app_from_request
from app.exceptions import ProductNotFound


class ProductPutSchema(BaseModel):
    title: str = None
    description: str = None
    cost: int = None
    category_uuid: UUID = None


async def products_put(request: Request, uuid: UUID, data: ProductPutSchema):
    app = get_app_from_request(request)

    product_data = data.model_dump()
    product_data = {key: value for key, value in product_data.items() if value is not None}
    try:
        product = app.update_product_by_uuid(uuid=uuid, **product_data)
    except ProductNotFound:
        return Response(status_code=404, content="Product not found")

    return product.__dict__
