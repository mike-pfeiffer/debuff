from fastapi import APIRouter
from debuff.api.routes import interfaces, tcconfig

router = APIRouter()

router.include_router(interfaces.router, tags=["interfaces"], prefix="/interfaces")
router.include_router(tcconfig.router, tags=["tc_show"], prefix="/tc_show")
