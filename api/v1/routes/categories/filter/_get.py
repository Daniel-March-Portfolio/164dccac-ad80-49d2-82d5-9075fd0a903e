from fastapi import Request

from api.v1.utils import get_app_from_request


async def categories_filter_get(request: Request, page: int, title: str = None, title__contains: str = None):
    app = get_app_from_request(request)

    categories_filter = {
        "title": title,
        "title__contains": title__contains
    }
    categories_filter = {key: value for key, value in categories_filter.items() if value is not None}
    categories = app.filter_categories(page=page, **categories_filter)

    return categories
