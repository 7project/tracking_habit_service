from fastapi import APIRouter
from api.views import router as user_router
from api.auth import router as jwt_router


router = APIRouter()
router.include_router(router=user_router, prefix="/user")
router.include_router(router=jwt_router, prefix="/jwt")
