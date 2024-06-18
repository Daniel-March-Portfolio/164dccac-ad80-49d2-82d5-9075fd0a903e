from fastapi import Request, Response
from pydantic import BaseModel

from api.v1.utils import get_app_from_request
from app.exceptions import AlreadyInUse


class CategoryPostSchema(BaseModel):
    title: str


async def categories_post(request: Request, data: CategoryPostSchema):
    app = get_app_from_request(request)

    try:
        category_uuid = app.create_category(**data.model_dump())
    except AlreadyInUse:
        return Response(status_code=409, content="Category has used params")

    return Response(content=str(category_uuid), status_code=201)
