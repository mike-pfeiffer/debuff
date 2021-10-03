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

import os
import re
import json
import subprocess


def set_ether_txqlen(interface: str, txqlen: int):
    cmd = f"sudo ip link set {interface} txqueuelen {txqlen}"
    subprocess.run(cmd, shell=True, stdout=open(os.devnull, 'wb'))
    value = show_ether_details(interface).get("txqlen")
    return value


def show_ether_details(interface: str):
    details = {}
    suffix = "_max"
    
    link_params = ["ifname", "mtu", "operstate", "txqlen", "address"]
    link_show = f"ip -j link show dev {interface}"
    link_output = subprocess.check_output(link_show, shell=True)
    link_detail = json.loads(link_output)[0]
    
    for key, value in link_detail.items():
        if key in link_params:
            details[key] = value

    ethtool_show = f"ethtool -g {interface}"
    ethtool_output = subprocess.check_output(ethtool_show, shell=True)
    ethtool_detail = ethtool_output.decode().split("\n")

    for line in ethtool_detail:
        line = line.lower()
        line = line.replace(":", "")
        line = line.replace(" ", "_")
        line = re.split("\t+", line)
        
        if "current" in line[0]:
            suffix = "_set"

        if len(line) == 2:
            key = line[0] + suffix
            value = int(line[1])
            details[key] = value

    return details


def show_all_ether_details() -> list:
    """
    """
    details = []
    ethernets = show_all_ether_names()
    for ethernet in ethernets:
        cmd = f"ip -j link show dev {ethernet}"
        output = subprocess.check_output(cmd, shell=True)
        output = json.loads(output)
        details.append(output) 
    return details


def show_all_iface_details() -> list:
    """
    """
    cmd = "ip -j link show"
    output = subprocess.check_output(cmd, shell=True)
    output = json.loads(output) 
    return output


def show_all_iface_names() -> list:
    """
    """
    interfaces = []

    iface_show = "ip -br -j link show"
    iface_list = subprocess.check_output(iface_show, shell=True)
    iface_dict = json.loads(iface_list)

    for iface in iface_dict:
        interfaces.append(iface["ifname"])

    return interfaces 


def show_all_ether_names() -> list:
    """
    """
    supported_ifaces = "^(eth|en[ops])"
    exclusion = "link"
    ethernets = []

    iface_show = "ip -br -j link show"
    iface_list = subprocess.check_output(iface_show, shell=True)
    iface_dict = json.loads(iface_list)

    for iface in iface_dict:
        if exclusion in iface:
            continue 
        if bool(re.search(supported_ifaces, iface["ifname"])):
            ethernets.append(iface["ifname"])

    return ethernets 


if __name__ == '__main__':
    show_ether_details("enp2s0")
