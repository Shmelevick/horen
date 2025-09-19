from fastapi import APIRouter

from .products.views import router as producs_router
from .demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(router=producs_router, prefix="/products")
router.include_router(router=demo_auth_router)
