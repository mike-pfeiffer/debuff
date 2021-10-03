from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from debuff.services.interfaces import * 

router = APIRouter()


@router.get("/names/all")
async def get_all_iface_names():
    result = show_all_iface_names()
    return result 


@router.get("/names/ethernet")
async def get_all_ether_names():
    result = show_all_ether_names()
    return result 


@router.get("/details/all")
async def get_all_iface_details():
    result = show_all_iface_details()
    return result


@router.get("/details")
async def get_ether_details(interface: str):
    result = show_ether_details(interface)
    return result 
