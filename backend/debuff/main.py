import uvicorn

from debuff.core.config import API_PREFIX, DEBUG, VERSION, PROJECT_NAME
from debuff.api.routes.api import router as api_router
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.include_router(api_router, prefix=API_PREFIX)

    return application

api = get_application()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("debuff.main:api", host="0.0.0.0", port=8000, reload=True)