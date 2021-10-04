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

import json
from debuff.services.shared_utilities import build_details, error_handling


def tcshow(interface: str):
    cmd_input = f"tcshow {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = cmd_output.decode()
        cmd_output = json.loads(cmd_output)

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def tcdel(interface: str):
    cmd_input = f"tcdel {interface} --all"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = tcshow(interface)["command_output"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def tcset(interface: str, delay: int, jitter: int, loss: int):
    cmd_input = (
        f"tcset {interface} --delay {delay}ms --delay-distro {jitter}ms "
        f"--loss {loss}"
    )
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = tcshow(interface)["command_output"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details
