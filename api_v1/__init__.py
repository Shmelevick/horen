from fastapi import APIRouter

from .products.views import router as producs_router

router = APIRouter()
router.include_router(router=producs_router, prefix="/products")
