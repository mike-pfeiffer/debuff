from fastapi import APIRouter
from debuff.api.routes import interfaces

router = APIRouter()

router.include_router(interfaces.router, tags=["interfaces"], prefix="/interfaces")