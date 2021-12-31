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

from debuff.models.enums import InterfaceEnum, DirectionsEnum
from debuff.services.impairments import (
    delete_interface_impairments,
    set_interface_impairments,
    show_interface_impairments,
)
from fastapi import APIRouter

router = APIRouter()


@router.get("/show")
async def tc_show(interface: InterfaceEnum):
    result = show_interface_impairments(interface)
    return result


@router.post("/set")
async def tc_set(
    interface: InterfaceEnum, direction: DirectionsEnum,
    delay: float = 0, jitter: float = 0, loss: float = 0,
    rate: float = 1000
):
    if direction == "bidirectional":
        split_delay = delay / 2
        split_jitter = jitter / 2
        split_loss = loss / 2
        set_interface_impairments(
            interface, "outgoing", split_delay, split_jitter, split_loss, rate
        )
        set_interface_impairments(
            interface, "incoming", split_delay, split_jitter, split_loss, rate
        )
        result = show_interface_impairments(interface)
    else:
        result = set_interface_impairments(
            interface, direction, delay, jitter, loss, rate
        )
    return result


@router.post("/delete")
async def tc_delete(interface: InterfaceEnum):
    result = delete_interface_impairments(interface)
    return result
