"""
An installer for the Debuff program.
Copyright (C) 2021 Mike Pfeiffer, Dustin Rosarius

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import uvicorn

from debuff.core.config import API_PREFIX, DEBUG, VERSION, PROJECT_NAME
from debuff.api.routes.api import router as api_router
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.include_router(api_router, prefix=API_PREFIX)

    return application


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("debuff.main:api", host="0.0.0.0", port=8002, reload=True)


api = get_application()
