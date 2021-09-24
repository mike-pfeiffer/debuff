from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from debuff.services.funcs import get_list_of_interfaces

router = APIRouter()


@router.get("")
async def get_interfaces():
    result = get_list_of_interfaces()
    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)
