from fastapi import APIRouter

from api.v1.routes.categories import router as categories_router
from api.v1.routes.products import router as products_router

router = APIRouter()
router.include_router(categories_router, prefix="/api/v1/categories")
router.include_router(products_router, prefix="/api/v1/products")
