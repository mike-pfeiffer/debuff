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

import yaml
from debuff.services.shared_utilities import build_details, error_handling

VLANS = "vlans"
BRIDGES = "bridges"
ETHERNETS = "ethernets"
COMMAND_OUTPUT = "command_output"


def get_netplan(setting: str = "all"):
    cmd_input = f"netplan get {setting}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        cmd_output = yaml.safe_load(cmd_output)

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details


def get_netplan_interfaces():
    cmd_input = [
        f"netplan get {VLANS}", f"netplan get {BRIDGES}", f"netplan get {ETHERNETS}"
    ]
    cmd_output = []
    error_msg = None
    is_errored = False

    netplan_vlans = get_netplan(VLANS)
    netplan_vlans = netplan_vlans[COMMAND_OUTPUT]

    netplan_bridges = get_netplan(BRIDGES)
    netplan_bridges = netplan_bridges[COMMAND_OUTPUT]

    netplan_ethernets = get_netplan(ETHERNETS)
    netplan_ethernets = netplan_ethernets[COMMAND_OUTPUT]

    if netplan_vlans is not None:
        for vlan in netplan_vlans:
            cmd_output.append(vlan)

    if netplan_bridges is not None:
        for bridge in netplan_bridges:
            cmd_output.append(bridge)

    if netplan_ethernets is not None:
        for ethernet in netplan_ethernets:
            cmd_output.append(ethernet)

    details = build_details(cmd_input, cmd_output, error_msg, is_errored)

    return details
