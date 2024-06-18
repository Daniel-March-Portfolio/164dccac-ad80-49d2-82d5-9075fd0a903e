from uuid import UUID

from fastapi import Request, Response

from api.v1.utils import get_app_from_request
from app.exceptions import ProductNotFound


async def products_delete(request: Request, uuid: UUID):
    app = get_app_from_request(request)

    try:
        app.delete_product_by_uuid(uuid=uuid)
    except ProductNotFound:
        return Response(status_code=404, content="Product not found")

    return Response(status_code=204, content="")
