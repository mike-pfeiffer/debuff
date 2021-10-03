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
from debuff.services.impairments import show_interface_impairments
from debuff.services.impairments import delete_interface_impairments
from debuff.services.impairments import set_interface_impairments

router = APIRouter()


@router.get("/show")
async def tc_show(interface: str):
    result = show_interface_impairments(interface)
    return result


@router.post("/set")
async def tc_set(interface: str, delay: int):
    result = set_interface_impairments(interface, delay)
    return result


@router.post("/delete")
async def tc_delete(interface: str):
    result = delete_interface_impairments(interface)
    return result
