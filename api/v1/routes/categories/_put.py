from uuid import UUID

from fastapi import Request, Response
from pydantic import BaseModel

from api.v1.utils import get_app_from_request
from app.exceptions import CategoryNotFound


class CategoryPutSchema(BaseModel):
    title: str = None


async def categories_put(request: Request, uuid: UUID, data: CategoryPutSchema):
    app = get_app_from_request(request)

    category_data = data.model_dump()
    category_data = {key: value for key, value in category_data.items() if value is not None}
    try:
        category = app.update_category_by_uuid(uuid=uuid, **category_data)
    except CategoryNotFound:
        return Response(status_code=404, content="Category not found")

    return category.__dict__
