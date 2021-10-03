from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from debuff.services.interfaces import * 

router = APIRouter()


@router.get("/details")
async def get_interface_details(interface: str):
    result = show_interface_details(interface)
    return result 
