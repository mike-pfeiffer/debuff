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
import re

from debuff.services.shell_ethtool import show_ring_buffers
from debuff.services.shell_ip_addr import ip_addr_show_dev
from debuff.services.shell_ip_link import ip_link_show_dev, ip_link_show_names
from debuff.services.shell_ip_route import ip_route_show


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
    interfaces = ip_link_show_names()["command_output"]
    for interface in interfaces:
        details = ip_link_show_dev(interface)["command_output"]
        if "txqlen" in details:
            tx = details["txqlen"]
            save_settings = f"ip link set dev {interface} txqueuelen {tx}"
            # TODO
            print(save_settings)


def save_ip_settings():
    interfaces = ip_link_show_names()["command_output"]

    for interface in interfaces:
        details = ip_addr_show_dev(interface)["command_output"]

        # interface with no address information
        if not details:
            continue

        # classify address as v4 or v6 for further testing
        for addr in details:
            family = addr["family"]
            net_addr = addr["local"]
            prefix = addr["prefixlen"]

            if family == "inet":
                ip_addr = ipaddress.IPv4Address(net_addr)
            elif family == "inet6":
                ip_addr = ipaddress.IPv6Address(net_addr)
            else:
                return 1

            test_is_loopback = ip_addr.is_loopback
            test_is_link_local = ip_addr.is_link_local
            test_is_multicast = ip_addr.is_multicast
            test_version = ip_addr.version

            if test_is_loopback or test_is_multicast:
                continue

            if test_is_link_local and test_version == 6:
                continue

            # TODO
            print(f"ip address add {ip_addr}/{prefix} dev {interface}")


def save_route_settings():
    routes = ip_route_show()["command_output"]

    for route in routes:
        if "gateway" in route:
            dst = route["dst"]
            gw = route["gateway"]
            # TODO
            print(f"ip route add {dst} via {gw}")


def write_save_file():
    return "TODO"


if __name__ == "__main__":
    save_ethtool_settings()
    save_txqlen_settings()
    save_ip_settings()
    save_route_settings()
