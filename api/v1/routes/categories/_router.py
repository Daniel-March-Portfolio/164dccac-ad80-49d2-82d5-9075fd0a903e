from fastapi import APIRouter

from api.v1.routes.categories._delete import categories_delete
from api.v1.routes.categories._get import categories_get
from api.v1.routes.categories._post import categories_post
from api.v1.routes.categories._put import categories_put
from api.v1.routes.categories.filter import router as filter_router

router = APIRouter()
router.add_api_route("/{uuid}", categories_delete, methods=["DELETE"])
router.add_api_route("/{uuid}", categories_get, methods=["GET"])
router.add_api_route("/", categories_post, methods=["POST"])
router.add_api_route("/{uuid}", categories_put, methods=["PUT"])

router.include_router(filter_router, prefix="/filter")
