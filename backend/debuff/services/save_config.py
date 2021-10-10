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

import yaml
from debuff.services.shell_ethtool import show_ring_buffers
from debuff.services.shell_ip_addr import ip_addr_show_all
from debuff.services.shell_ip_link import ip_link_show_names
from debuff.services.shell_ip_route import ip_route_show

KEY_ID = "id"
KEY_NETWORK = "network"
KEY_BRIDGES = "bridges"
KEY_VLANS = "vlans"
KEY_ETHERNETS = "ethernets"
KEY_IFNAME = "ifname"
KEY_LINKINFO = "linkinfo"
KEY_LINK_TYPE = "link_type"
KEY_INFO_KIND = "info_kind"
KEY_INFO_DATA = "info_data"
KEY_ADDR_INFO = "addr_info"


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


def parse_addr_info(addr_info: list):
    addr_list = []

    for addr in addr_info:
        if "dynamic" in addr:
            # TODO
            print("hi")
        ip = addr["local"]
        prefix = addr["prefixlen"]
        address = f"{ip}/{prefix}"
        addr_list.append(address)

    return addr_list


def parse_routes(ifname: str, routes: list) -> list:
    routes_list = []

    for route in routes:
        if "gateway" in route and ifname == route["dev"]:
            if route["dst"] == "default":
                route_dict = {"to": "0.0.0.0/0", "via": route["gateway"]}
            else:
                route_dict = {"to": route["dst"], "via": route["gateway"]}
            routes_list.append(route_dict)

    return routes_list


def create_ethernet_dict(interface, routes):
    """
    Extract the interface name and parse the IPv4/IPv6 address(es), if any,
    for the interface.
    """
    ethernet_dict = {}
    ifname = interface[KEY_IFNAME]
    addr_info = interface[KEY_ADDR_INFO]
    addresses = parse_addr_info(addr_info)
    link_routes = parse_routes(ifname, routes)

    if addresses:
        ethernet_dict["addresses"] = addresses

    if link_routes:
        ethernet_dict["routes"] = link_routes

    return ethernet_dict


def create_bridge_dict(interface, routes):
    """
    Extract the interface name and parse the IPv4/IPv6 address(es), if any,
    for the interface.
    """
    bridge_dict = {}
    ifname = interface[KEY_IFNAME]
    addr_info = interface[KEY_ADDR_INFO]
    addresses = parse_addr_info(addr_info)
    link_routes = parse_routes(ifname, routes)

    if addresses:
        bridge_dict["addresses"] = addresses

    if link_routes:
        bridge_dict["routes"] = link_routes

    return bridge_dict


def create_vlan_dict(interface, routes):
    """
    Extract the interface name and parse the IPv4/IPv6 address(es), if any,
    for the interface.
    """
    vlan_dict = {}
    ifname = interface[KEY_IFNAME]
    addr_info = interface[KEY_ADDR_INFO]
    addresses = parse_addr_info(addr_info)
    linkinfo = interface[KEY_LINKINFO]
    info_data = linkinfo[KEY_INFO_DATA]
    link_routes = parse_routes(ifname, routes)
    vid = info_data[KEY_ID]
    parent = interface["link"]
    vlan_dict["id"] = vid
    vlan_dict["link"] = parent

    if addresses:
        vlan_dict["addresses"] = addresses

    if link_routes:
        vlan_dict["routes"] = link_routes

    return vlan_dict


def create_netplan():
    netplan = {KEY_NETWORK: {"version": 2}}
    allowed_link_type = ["ether"]
    routes = ip_route_show()["command_output"]
    interfaces = ip_addr_show_all()["command_output"]

    for interface in interfaces:
        link_type = interface[KEY_LINK_TYPE]

        """
        The 'loopback' interface is not currently supported in this release and
        only the 'ether' type is permitted.
        """
        if link_type not in allowed_link_type:
            continue

        ifname = interface[KEY_IFNAME]

        """
        The 'linkinfo' key is present in the command output for bridge and VLAN
        interface(s).
        """
        if KEY_LINKINFO in interface:

            """
            To determine VLAN or bridge a nested dict needs to be parsed from
            output. Example: "linkinfo": {"info_kind": "bridge"}.
            """
            linkinfo = interface[KEY_LINKINFO]
            info_kind = linkinfo[KEY_INFO_KIND]

            if info_kind == "bridge":

                if KEY_BRIDGES not in netplan[KEY_NETWORK]:
                    netplan[KEY_NETWORK][KEY_BRIDGES] = {}

                bridge_dict = create_bridge_dict(interface, routes)
                netplan[KEY_NETWORK][KEY_BRIDGES][ifname] = bridge_dict

            elif info_kind == "vlan":

                if KEY_VLANS not in netplan[KEY_NETWORK]:
                    netplan[KEY_NETWORK][KEY_VLANS] = {}

                vlan_dict = create_vlan_dict(interface, routes)
                netplan[KEY_NETWORK][KEY_VLANS][ifname] = vlan_dict

        else:

            if KEY_ETHERNETS not in netplan[KEY_NETWORK]:
                netplan[KEY_NETWORK][KEY_ETHERNETS] = {}

            ethernet_dict = create_ethernet_dict(interface, routes)
            netplan[KEY_NETWORK][KEY_ETHERNETS][ifname] = ethernet_dict

    print(yaml.dump(netplan))


def write_save_file():
    return "TODO"


if __name__ == "__main__":
    create_netplan()
