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
from debuff.services.linux_tools import ethtool_check_ring_buffers
from debuff.services.linux_tools import ip_addr_show_dev
from debuff.services.linux_tools import ip_link_show_names


def show_interface_buffers(interface: str):
    """
    """
    ethtool_detail = ethtool_check_ring_buffers(interface)
    if ethtool_detail["is_errored"]:
        cmd_input = ethtool_detail["command_input"]
        cmd_output = ethtool_detail["command_output"]
        errors = ethtool_detail["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = {f"{interface}": ethtool_detail["command_output"]}

    return payload


def show_interface_details(interface: str):
    """
    """
    link_detail = ip_addr_show_dev(interface)

    if link_detail["is_errored"]:
        cmd_input = link_detail["command_input"]
        cmd_output = link_detail["command_output"]
        errors = link_detail["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    ifname = link_detail["command_output"].pop("ifname")
    payload = {f"{ifname}": link_detail["command_output"]}

    return payload


def show_all_interface_names() -> list:
    """
    """
    iface_names = ip_link_show_names()

    if iface_names["is_errored"]:
        cmd_input = iface_names["command_input"]
        cmd_output = iface_names["command_output"]
        errors = iface_names["error_message"]
        return error_response(cmd_input, cmd_output, errors)

    payload = iface_names["command_output"]

    return payload
