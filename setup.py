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

import subprocess


def apt_update():
    subprocess.run("apt update", shell=True)


def install_pip():
    check_pip = "pip --version"
    install_pip = "apt-get install python3-pip"
    try:
        subprocess.check_output(check_pip, shell=True)
        print("> pip installation check complete")
    except subprocess.CalledProcessError:
        print("> installing python3-pip")
        subprocess.run(install_pip, shell=True)
        print("> python3-pip installation complete")


def install_networking():
    sysctl_conf = "/etc/sysctl.conf"
    ipv4_fwd = "net.ipv4.ip_forward = 1"
    ipv6_fwd = "net.ipv6.conf.all.forwarding=1"
    subprocess.run(f"echo {ipv4_fwd} >> {sysctl_conf}", shell=True)
    subprocess.run(f"echo {ipv6_fwd} >> {sysctl_conf}", shell=True)
    subprocess.run("sysctl -p", shell=True)
    subprocess.run("apt-get install bridge-utils", shell=True)
    subprocess.run("apt-get install vlan", shell=True)
    subprocess.run("modprobe 8021q", shell=True)


def install_tcconfig():
    subprocess.run("pip install tcconfig", shell=True)


if __name__ == '__main__':
    apt_update()
    install_pip()
    install_networking()
    install_tcconfig()
