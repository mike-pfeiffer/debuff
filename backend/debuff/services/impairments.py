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

from debuff.services.parser import error_response
from debuff.services.shell_commands import tcshow
from debuff.services.shell_commands import tcdel
from debuff.services.shell_commands import tcset


def show_interface_impairments(interface: str):
    iface_impairments = tcshow(interface)

    if iface_impairments["is_errored"]:
        cmd_input = iface_impairments["command_input"]
        cmd_output = iface_impairments["command_output"]
        errors = iface_impairments["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = iface_impairments["command_output"]

    return payload


def delete_interface_impairments(interface: str):
    delete_impairments = tcdel(interface)

    if delete_impairments["is_errored"]:
        cmd_input = delete_impairments["command_input"]
        cmd_output = delete_impairments["command_output"]
        errors = delete_impairments["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = delete_impairments["command_output"]

    return payload


def set_interface_impairments(interface: str, delay: int = 0):
    set_impairments = tcset(interface, delay)

    if set_impairments["is_errored"]:
        cmd_input = set_impairments["command_input"]
        cmd_output = set_impairments["command_output"]
        errors = set_impairments["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = set_impairments["command_output"]

    return payload
