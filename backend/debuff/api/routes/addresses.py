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
from debuff.services.addresses import show_inet_address
from debuff.services.addresses import set_inet_address
from debuff.services.addresses import delete_inet_address

router = APIRouter()


@router.get("/show")
async def interface_ip_show(interface: str):
    result = show_inet_address(interface)
    return result


@router.post("/set")
async def interface_ip_set(interface: str, ip: str, prefix_len: int):
    result = set_inet_address(interface, ip, prefix_len)
    return result


@router.post("/delete")
async def interface_ip_delete(interface: str, ip: str, prefix_len: int):
    result = delete_inet_address(interface, ip, prefix_len)
    return result
