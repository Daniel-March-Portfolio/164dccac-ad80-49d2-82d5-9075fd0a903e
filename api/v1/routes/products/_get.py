from uuid import UUID

from fastapi import Request, Response

from api.v1.utils import get_app_from_request
from app.exceptions import ProductNotFound


async def products_get(request: Request, uuid: UUID):
    app = get_app_from_request(request)

    try:
        product = app.get_product(uuid)
    except ProductNotFound:
        return Response(status_code=404, content="Product not found")

    print(product)
    return product.__dict__
