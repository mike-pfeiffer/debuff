#!/usr/bin/python3
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
import sys
import json
import platform
import subprocess
import lsb_release


def validate_os():
    """Exits script if invalid OS detected for Debuff install."""

    # section for platform, distro, version support
    supported_platforms = ["Linux"]
    supported_distros = ["Ubuntu"]
    ubuntu_min = "18"

    this_platform = platform.system()

    # platform check
    if(this_platform not in supported_platforms):
        sys.exit(f"Debuff is not supported on {this_platform}.")

    os_info = lsb_release.get_distro_information()
    os_id = os_info["ID"]

    # distro check
    if(os_id not in supported_distros):
        sys.exit(f"Debuff has not been validated on {os_id}.")

    os_release = os_info["RELEASE"]

    # version check for ubuntu
    if(os_id == supported_distros[0] and os_release < ubuntu_min):
        sys.exit(f"Debuff minimum {os_id} version must be {ubuntu_min}.")


def set_management():
    """Return valid interface Debuff management."""

    # regex for ethernet/wireless devices
    supported_ifaces = "^(wl|en)[ops]"
    mgmt_options = []

    # run shell command to view links in json
    iface_show = "ip -br -j link show"
    iface_list = subprocess.check_output(iface_show, shell=True)
    iface_dict = json.loads(iface_list)

    # extract and append valid interfaces
    for iface in iface_dict:
        if(bool(re.search(supported_ifaces, iface["ifname"]))):
            mgmt_options.append(iface["ifname"])

    if(len(mgmt_options) == 0):
        sys.exit("A valid Ethernet or Wireless adapter was not found.")

    print("Select management interface: " + str(mgmt_options))

    while True:
        mgmt_iface = input("Enter interface name: ")
        if(mgmt_iface in mgmt_options):
            break
        else:
            print(f"{mgmt_iface} is not a valid option, try again.")

    return mgmt_iface


if __name__ == '__main__':
    validate_os()
    set_management()
