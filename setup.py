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
import subprocess


def apt_update():
    print("=> Starting apt update")
    subprocess.run(
        "sudo apt-get update", shell=True, stdout=open(os.devnull, 'wb')
    )
    print("=> Completed apt update")


def install_pip():
    print("=> Starting pip install")
    check_pip = "pip --version"
    install_pip = "sudo apt-get install python3-pip"

    try:
        subprocess.check_output(check_pip, shell=True)
    except subprocess.CalledProcessError:
        subprocess.run(install_pip, shell=True, stdout=open(os.devnull, 'wb'))

    print("=> Completed pip install")


def install_networking():
    print("=> Starting networking install")
    sysctl_conf = "/etc/sysctl.conf"
    ipv4_fwd_status = "cat /proc/sys/net/ipv4/ip_forward"
    ipv6_fwd_status = "cat /proc/sys/net/ipv6/conf/all/forwarding"
    ipv4_fwd_enable = "net.ipv4.ip_forward = 1"
    ipv6_fwd_enable = "net.ipv6.conf.all.forwarding = 1"

    # check if ipv4 forwarding is enabled
    ipv4_fwd = subprocess.check_output(ipv4_fwd_status,
                                       shell=True).decode("utf-8").rstrip()
    if ipv4_fwd == "0":
        subprocess.run(f"echo {ipv4_fwd_enable} >> {sysctl_conf}", shell=True)

    # check if ipv6 forwarding is enabled
    ipv6_fwd = subprocess.check_output(ipv6_fwd_status,
                                       shell=True).decode("utf-8").rstrip()
    if ipv6_fwd == "0":
        subprocess.run(f"echo {ipv6_fwd_enable} >> {sysctl_conf}", shell=True)

    # load sysctl.conf, install bridge-utils & vlan, enable 802.1q
    args = [
        "sysctl -p", "sudo apt-get install bridge-utils",
        "sudo apt-get install vlan", "modprobe 8021q"
    ]

    for arg in args:
        subprocess.run(arg, shell=True, stdout=open(os.devnull, 'wb'))

    print("=> Completed networking install")


def install_tcconfig():
    print("=> Starting tcconfig install")
    subprocess.run("sudo pip install tcconfig", shell=True,
                   stdout=open(os.devnull, 'wb'))
    print("=> Completed tcconfig install")


def set_permissions():
    print("=> Started setting permissions")
    subprocess.run(
        "echo $USER ALL=NOPASSWD: /usr/sbin/ip | sudo EDITOR='tee -a' visudo",
        shell=True, stdout=open(os.devnull, 'wb')
    )
    subprocess.run(
        "echo $USER ALL=NOPASSWD: /usr/sbin/tc | sudo EDITOR='tee -a' visudo",
        shell=True, stdout=open(os.devnull, 'wb')
    )
    subprocess.run(
        "echo $USER ALL=NOPASSWD: /usr/sbin/ethtool | sudo EDITOR='tee -a' visudo",
        shell=True, stdout=open(os.devnull, 'wb')
    )
    print("=> Completed setting permissions")


if __name__ == '__main__':
    apt_update()
    install_pip()
    install_networking()
    install_tcconfig()
    set_permissions()
