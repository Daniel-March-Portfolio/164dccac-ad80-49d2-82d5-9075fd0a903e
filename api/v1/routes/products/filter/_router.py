from fastapi import APIRouter

from api.v1.routes.products.filter._get import products_filter_get

router = APIRouter()
router.add_api_route("/", products_filter_get, methods=["GET"])
