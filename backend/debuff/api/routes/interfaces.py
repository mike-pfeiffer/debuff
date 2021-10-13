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

from debuff.models.enums import InterfaceEnum, InterfaceStateEnum
from debuff.services.interfaces import (
    set_interface_buffers,
    set_interface_state,
    show_all_interface_names,
    show_interface_buffers,
    show_interface_details,
)
from fastapi import APIRouter

router = APIRouter()


@router.get("/details")
async def get_interface_details(interface: InterfaceEnum):
    result = show_interface_details(interface)
    return result


@router.get("/buffers")
async def get_interface_buffers(interface: InterfaceEnum):
    result = show_interface_buffers(interface)
    return result


@router.get("/names")
async def get_interface_names():
    result = show_all_interface_names()
    return result


@router.post("/state")
async def post_interface_state(interface: InterfaceEnum, state: InterfaceStateEnum):
    result = set_interface_state(interface, state)
    return result


@router.post("/buffers")
async def post_interface_buffers(interface: InterfaceEnum, rx_ring: int, tx_ring: int):
    result = set_interface_buffers(interface, rx_ring, tx_ring)
    return result
