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

from debuff.models.TcModel import TcSetValues
from debuff.services.impairments import (
    delete_interface_impairments,
    set_interface_impairments,
    show_interface_impairments,
)
from fastapi import APIRouter

router = APIRouter()


@router.get("/show")
async def tc_show(interface: str):
    result = show_interface_impairments(interface)
    return result


@router.post("/set")
async def tc_set(tcset_values: TcSetValues):
    if tcset_values.direction == "bidirectional":
        split_delay = tcset_values.delay / 2
        split_jitter = tcset_values.jitter / 2
        split_loss = tcset_values.loss / 2
        set_interface_impairments(
            tcset_values.interface, "outgoing", split_delay, split_jitter, split_loss
        )
        set_interface_impairments(
            tcset_values.interface, "incoming", split_delay, split_jitter, split_loss
        )
        result = show_interface_impairments(tcset_values.interface)
    else:
        result = set_interface_impairments(
            tcset_values.interface,
            tcset_values.direction,
            tcset_values.delay,
            tcset_values.jitter,
            tcset_values.loss,
        )
    return result


@router.post("/delete")
async def tc_delete(interface: str):
    result = delete_interface_impairments(interface)
    return result
