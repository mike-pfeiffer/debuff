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

import ipaddress
import json

from debuff.services.shared_utilities import build_details, error_handling


def ip_addr_del_dev(interface: str, ip: str, prefix_len: int):
    cmd_input = f"ip addr del {ip}/{prefix_len} dev {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = ip_addr_show_dev(interface)["command_output"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def ip_addr_add_dev(interface: str, ip: str, prefix_len: int):
    assigned_addrs = ip_addr_show_dev(interface)["command_output"]

    try:
        ip_type = ipaddress.ip_address(ip)
        is_ipv4 = isinstance(ip_type, ipaddress.IPv4Address)
        is_ipv6 = isinstance(ip_type, ipaddress.IPv6Address)
    except ValueError as e:
        details = build_details(None, None, e, True)
        return details

    for addrs in assigned_addrs:
        if is_ipv4 and addrs["family"] == "inet":
            ip_addr_del_dev(interface, addrs["local"], addrs["prefixlen"])
            break
        if is_ipv6 and addrs["family"] == "inet6" and addrs["scope"] == "global":
            ip_addr_del_dev(interface, addrs["local"], addrs["prefixlen"])
            break

    cmd_input = f"ip addr add {ip}/{prefix_len} dev {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = ip_addr_show_dev(interface)["command_output"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def ip_addr_show_dev(interface: str):
    cmd_input = f"ip -j addr show dev {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = json.loads(cmd_output)[0]["addr_info"]

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def ip_addr_show_all():
    cmd_input = "ip -json -details address show"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = json.loads(cmd_output)

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details
