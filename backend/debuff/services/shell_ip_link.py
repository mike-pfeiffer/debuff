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

import ast
import json

from debuff.services.shared_utilities import build_details, error_handling


def ip_link_show_dev(interface: str):
    cmd_input = f"ip -j link show dev {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = json.loads(cmd_output)[0]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def ip_link_set_state(interface: str, state: str):
    cmd_input = f"ip link set {interface} {state}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = ip_link_show_dev(interface)["command_output"]["operstate"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def ip_link_show_names():
    cmd_input = "ip -j link show"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        new_list = []
        cmd_output = ast.literal_eval(cmd_output.decode())
        for interface in cmd_output:
            new_list.append(interface["ifname"])
        cmd_output = new_list

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details
