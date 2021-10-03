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

from fastapi import APIRouter
from debuff.services.interfaces import show_interface_details
from debuff.services.interfaces import show_interface_buffers
from debuff.services.interfaces import show_all_interface_names


router = APIRouter()


@router.get("/details")
async def get_interface_details(interface: str):
    result = show_interface_details(interface)
    return result


@router.get("/buffers")
async def get_interface_buffers(interface: str):
    result = show_interface_buffers(interface)
    return result


@router.get("/names")
async def get_interface_names():
    result = show_all_interface_names()
    return result
