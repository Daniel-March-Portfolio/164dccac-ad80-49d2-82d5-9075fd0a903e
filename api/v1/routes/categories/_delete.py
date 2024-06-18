from uuid import UUID

from fastapi import Request, Response

from api.v1.utils import get_app_from_request
from app.exceptions import CategoryNotFound


async def categories_delete(request: Request, uuid: UUID):
    app = get_app_from_request(request)

    try:
        app.delete_category_by_uuid(uuid=uuid)
    except CategoryNotFound:
        return Response(status_code=404, content="Category not found")

    return Response(status_code=204, content="")
