from fastapi import APIRouter

from api.v1.routes.categories.filter._get import categories_filter_get

router = APIRouter()
router.add_api_route("/", categories_filter_get, methods=["GET"])
