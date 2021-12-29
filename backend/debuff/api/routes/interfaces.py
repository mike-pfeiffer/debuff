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
from debuff.services.impairments import show_interface_impairments
from debuff.services.interfaces import (
    set_interface_state,
    show_all_interface_names,
    show_interface_details,
)
from fastapi import APIRouter

router = APIRouter()


@router.get("/names")
async def get_interface_names():
    result = show_all_interface_names()
    return result


@router.get("/state")
async def get_interface_state(interface: InterfaceEnum):
    impaired_status = show_interface_impairments(interface)[interface]
    if (impaired_status["outgoing"] or impaired_status["incoming"]):
        result = "IMPAIRED"
    else:
        result = show_interface_details(interface)[interface]["operstate"]
    return result


@router.post("/state")
async def post_interface_state(interface: InterfaceEnum, state: InterfaceStateEnum):
    result = set_interface_state(interface, state)
    return result
