from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from debuff.services.funcs import tcshow
import json

router = APIRouter()

@router.get("")
async def tc_show(interface: str):
    result = json.loads(tcshow(interface))
    json_result = jsonable_encoder(result)
    return json_result


