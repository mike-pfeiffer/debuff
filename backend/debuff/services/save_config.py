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

import re

from debuff.services.shell_ethtool import show_ring_buffers
from debuff.services.shell_ip_link import ip_link_show_names


def save_ethtool_settings():
    ethernets = []
    allowed_pnids = "^en[ops][0-9][a-z]?[0-9]?$"
    interfaces = ip_link_show_names()["command_output"]

    for interface in interfaces:
        is_ethernet = bool(re.search(allowed_pnids, interface))
        if is_ethernet:
            ethernets.append(interface)

    for ethernet in ethernets:
        ring_settings = show_ring_buffers(ethernet)["command_output"]
        rx = ring_settings["rx_ring_set"]
        tx = ring_settings["tx_ring_set"]
        save_settings = f"ethtool -G {ethernet} rx {rx} tx {tx}"
        # TODO
        print(save_settings)


def save_txqlen_settings():
    return "TODO"


def save_ip_settings():
    return "TODO"


def save_route_settings():
    return "TODO"


def write_save_file():
    return "TODO"


if __name__ == "__main__":
    save_ethtool_settings()
