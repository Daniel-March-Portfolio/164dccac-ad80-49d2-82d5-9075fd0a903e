from fastapi import APIRouter

from api.v1.routes.products._delete import products_delete
from api.v1.routes.products._get import products_get
from api.v1.routes.products._post import products_post
from api.v1.routes.products._put import products_put
from api.v1.routes.products.filter import router as filter_router

router = APIRouter()
router.add_api_route("/{uuid}", products_delete, methods=["DELETE"])
router.add_api_route("/{uuid}", products_get, methods=["GET"])
router.add_api_route("/", products_post, methods=["POST"])
router.add_api_route("/{uuid}", products_put, methods=["PUT"])

router.include_router(filter_router, prefix="/filter")
