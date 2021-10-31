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

import os
import stat
import subprocess

import yaml

VLANS = "vlans"
NETWORK = "network"
ETHERNETS = "ethernets"


def get_netplan():
    cmd = "netplan get all"
    output = subprocess.check_output(cmd, shell=True)
    output = yaml.safe_load(output)
    output = output[NETWORK]
    return output


def get_ring_buffers(iface: str):
    cmd = f"ethtool -g {iface}"
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    output = output.split("\n")

    ring_buffers = {}
    temp_key = ""
    temp_dict = {}

    # The first line is not needed the returned dictionary.
    for entry in output[1:]:
        entry = entry.split(":")

        # The ethtool output contains two empty lines at the end.
        if len(entry) == 1:
            break

        # This creates top level key based on value-less entry.
        if not entry[1]:
            temp_key = entry[0]
            temp_dict = {}
            ring_buffers[temp_key] = temp_dict
            continue

        # Builds the nested dictionary of ring parameter values.
        value = entry[1].strip("\t")
        temp_dict[entry[0]] = value

    return ring_buffers


def setup_interfaces():
    netplan = get_netplan()
    service_path = "/etc/networkd-dispatcher/routable.d/"
    service_file = "50-ifup-hooks"
    filename = service_path + service_file
    data = "#!/bin/bash"
    txqueuelen = "2500"

    with open(filename, "w") as f:

        if ETHERNETS in netplan:
            ethernets = netplan[ETHERNETS]

            for iface in ethernets.keys():
                # Set ring buffers to max to avoid packet drops.
                maximum = get_ring_buffers(iface)["Pre-set maximums"]
                max_rx = maximum["RX"]
                max_rx_mini = maximum["RX Mini"]
                max_rx_jumbo = maximum["RX Jumbo"]
                max_tx = maximum["TX"]
                rings = (
                    f"ethtool -G {iface} rx {max_rx} rx-mini {max_rx_mini} "
                    f"rx-jumbo {max_rx_jumbo} tx {max_tx}"
                )
                data += f"\n{rings}"

                # Increase standard 1000 txqueuelen to avoid overflow drops.
                queuelen = f"ip link set txqueuelen {txqueuelen} dev {iface}"
                data += f"\n{queuelen}"

        if VLANS in netplan:
            vlans = netplan[VLANS]

            for iface in vlans.keys():
                # Increase standard 1000 txqueuelen to avoid overflow drops.
                queuelen = f"ip link set txqueuelen {txqueuelen} dev {iface}"
                data += f"\n{queuelen}"

        # Add a newline to EOF and write the settings out to the file.
        data += "\n"
        f.write(data)

    # Make file executable so that it runs on boot.
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def setup_routing():
    sysctl_conf = "/etc/sysctl.conf"
    ipv4_fwd_status = "cat /proc/sys/net/ipv4/ip_forward"
    ipv6_fwd_status = "cat /proc/sys/net/ipv6/conf/all/forwarding"
    ipv4_fwd_enable = "net.ipv4.ip_forward = 1"
    ipv6_fwd_enable = "net.ipv6.conf.all.forwarding = 1"

    # check if ipv4 forwarding is enabled
    ipv4_fwd = (
        subprocess.check_output(ipv4_fwd_status, shell=True).decode("utf-8").rstrip()
    )
    if ipv4_fwd == "0":
        subprocess.run(f"echo {ipv4_fwd_enable} >> {sysctl_conf}", shell=True)

    # check if ipv6 forwarding is enabled
    ipv6_fwd = (
        subprocess.check_output(ipv6_fwd_status, shell=True).decode("utf-8").rstrip()
    )
    if ipv6_fwd == "0":
        subprocess.run(f"echo {ipv6_fwd_enable} >> {sysctl_conf}", shell=True)

    arg = "sysctl -p"
    subprocess.run(arg, shell=True, stdout=open(os.devnull, "wb"))


def apt_update():
    print("=^ Starting apt update")
    subprocess.run("apt-get update", shell=True, stdout=open(os.devnull, "wb"))
    print("=$ Completed apt update")


def install_pip():
    print("=^ Starting pip install")
    check_pip = "pip --version"
    install_pip = "apt-get install python3-pip"

    try:
        subprocess.check_output(check_pip, shell=True)
    except subprocess.CalledProcessError:
        subprocess.run(install_pip, shell=True, stdout=open(os.devnull, "wb"))

    print("=$ Completed pip install")


def install_networking():
    print("=^ Starting networking install")

    # load sysctl.conf, install bridge-utils & vlan, enable 802.1q
    print(".. installing networking utilities")
    args = [
        "apt-get install bridge-utils",
        "apt-get install vlan",
        "modprobe 8021q",
    ]

    for arg in args:
        subprocess.run(arg, shell=True, stdout=open(os.devnull, "wb"))

    print(".. activating ipv4, ipv6 forwarding")
    setup_routing()

    print(".. optimizing interface buffers, txqueues")
    setup_interfaces()

    print("=$ Completed networking install")


def install_tcconfig():
    print("=^ Starting tcconfig install")
    subprocess.run(
        "pip install tcconfig", shell=True, stdout=open(os.devnull, "wb")
    )
    print("=$ Completed tcconfig install")


def install_debuff():
    # TODO
    return None


if __name__ == "__main__":
    apt_update()
    install_pip()
    install_networking()
    install_tcconfig()
    install_debuff()
