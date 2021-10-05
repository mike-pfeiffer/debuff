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

from debuff.services.shared_utilities import error_response
from debuff.services.shell_ip_addr import ip_addr_show_dev


def show_inet_address(interface: str):
    """
    """
    details = ip_addr_show_dev(interface)

    if details["is_errored"]:
        cmd_input = details["command_input"]
        cmd_output = details["command_output"]
        errors = details["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = details["command_output"]

    return payload
