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
from debuff.services.parser import error_response
from debuff.services.linux_tools import *
#from parser import error_response
#from linux_tools import *


#def set_ether_txqlen(interface: str, txqlen: int):
#    cmd_input = f"sudo ip link set {interface} txqueuelen {txqlen}"
#    cmd_output = subprocess.check_output(cmd_input, shell=True)
#    details = show_ether_details(interface).get("txqlen")
#    response = response_body(cmd_input, cmd_output, details)
#    return response


def show_interface_details(interface: str):
    """
    """
    data = {}
    cmd_input = []
    cmd_output = []
    errors = []

    link_detail = ip_addr_show_dev(interface)
    ethtool_detail = ethtool_check_ring_buffers(interface)
   
    if (link_detail["is_errored"] or ethtool_detail["is_errored"]):
        cmd_input.append(link_detail["command_input"])
        cmd_input.append(ethtool_detail["command_input"])
        cmd_output.append(link_detail["command_output"])
        cmd_output.append(ethtool_detail["command_output"])
        errors.append(link_detail["error_message"])
        errors.append(ethtool_detail["error_message"])
        return error_response(cmd_input, cmd_output, errors) 

    ifname = link_detail["command_output"].pop("ifname")

    data = {
        **link_detail["command_output"],
        **ethtool_detail["command_output"]
    }

    payload = {f"{ifname}": data}

    return payload


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
    #print(ethtool_check_ring_buffers("enp2s0"))
    print(show_interface_details("enp2s0"))
