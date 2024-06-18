from uuid import UUID

from fastapi import Request, Query

from api.v1.utils import get_app_from_request


async def products_filter_get(
        request: Request, page: int, title: str = None, description: str = None, cost: int = None,
        category_uuid: UUID = None, title__not_in: list[str] = Query(None), title__in: list[str] = Query(None),
        title__not_equal: list[str] = Query(None), title__contains: str = None,
        description__not_in: list[str] = Query(None), description__in: list[str] = Query(None),
        description__not_equal: list[str] = Query(None), description__contains: str = None,
        cost__lower_than: int = None, cost__lower_than_or_equal_to: int = None, cost__greater_than: int = None,
        cost__greater_than_or_equal_to: int = None, cost__not_in: list[int] = Query(None),
        cost__in: list[int] = Query(None), cost__not_equal: int = None, category_uuid__not_in: list[UUID] = Query(None),
        category_uuid__in: list[UUID] = Query(None), category_uuid__not_equal: UUID = None
):
    app = get_app_from_request(request)

    products_filter = {
        "title": title,
        "description": description,
        "cost": cost,
        "category_uuid": category_uuid,
        "title__not_in": title__not_in,
        "title__in": title__in,
        "title__not_equal": title__not_equal,
        "title__contains": title__contains,
        "description__not_in": description__not_in,
        "description__in": description__in,
        "description__not_equal": description__not_equal,
        "description__contains": description__contains,
        "cost__lower_than": cost__lower_than,
        "cost__lower_than_or_equal_to": cost__lower_than_or_equal_to,
        "cost__greater_than": cost__greater_than,
        "cost__greater_than_or_equal_to": cost__greater_than_or_equal_to,
        "cost__not_in": cost__not_in,
        "cost__in": cost__in,
        "cost__not_equal": cost__not_equal,
        "category_uuid__not_in": category_uuid__not_in,
        "category_uuid__in": category_uuid__in,
        "category_uuid__not_equal": category_uuid__not_equal,
    }
    products_filter = {key: value for key, value in products_filter.items() if value is not None}
    print(products_filter)
    products = app.filter_products(page=page, **products_filter)

    return products
