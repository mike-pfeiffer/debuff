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
import yaml
import subprocess

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
    print("^ Starting apt update")
    subprocess.run("apt-get update", shell=True, stdout=open(os.devnull, "wb"))
    print("$ Completed apt update")


def install_pip():
    print("^ Starting pip install")
    check_pip = "pip --version"
    install_pip = "apt-get install python3-pip"

    try:
        subprocess.check_output(check_pip, shell=True)
    except subprocess.CalledProcessError:
        subprocess.run(install_pip, shell=True, stdout=open(os.devnull, "wb"))

    print("$ Completed pip install")


def install_networking():
    print("^ Starting networking install")

    # load sysctl.conf, install bridge-utils & vlan, enable 802.1q
    print("+ installing networking utilities")
    args = [
        "apt-get install bridge-utils",
        "apt-get install vlan",
        "modprobe 8021q",
    ]

    for arg in args:
        subprocess.run(arg, shell=True, stdout=open(os.devnull, "wb"))

    print("+ activating ipv4, ipv6 forwarding")
    setup_routing()

    print("+ optimizing interface buffers, txqueues")
    setup_interfaces()

    print("$ Completed networking install")


def install_requirements():
    print("^ Starting python requirements install")
    subprocess.run(
        "pip install -r requirements.txt", shell=True, stdout=open(os.devnull, "wb")
    )
    print("$ Completed python requirements install")


def install_debuff():
    print("^ Starting debuff install")

    directory = os.getcwd()
    service_path = "/etc/systemd/system/"
    boot_files = ["boot_backend.sh", "boot_frontend.sh"]
    service_files = ["debuff_backend.service", "debuff_frontend.service"]

    args = [
        "poetry install",
        "apt-get install npm",
        f"npm install --prefix {directory}/frontend/debuff/"
    ]

    print("+ setting up poetry and npm")
    # for arg in args:
    #    subprocess.run(arg, shell=True, stdout=open(os.devnull, "wb"))

    print("+ creating startup files")

    # Write the boot file for the backend.
    with open(boot_files[0], "w") as f:
        content = (
            "#!/bin/bash\n",
            f"cd {directory}\n",
            f"poetry run start\n"
        )

        for line in content:
            f.write(line)

    # Write the boot file for the front.
    with open(boot_files[1], "w") as f:
        content = (
            "#!/bin/bash\n",
            f"npm run serve --prefix {directory}/frontend/debuff/\n"
        )

        for line in content:
            f.write(line)

    for service_file in service_files:
        if service_file == service_files[0]:
            boot_file = boot_files[0]

        if service_file == service_files[1]:
            boot_file = boot_files[1]

        service_contents = (
            f"[Unit]\n",
            f"Description=Debuff\n",
            f"After=network.target\n",
            f"StartLimitIntervalSec=0\n\n",
            f"[Service]\n",
            f"Type=simple\n",
            f"User=root\n",
            f"ExecStart={directory}/{boot_file}\n\n",
            f"[Install]\n",
            f"WantedBy=multi-user.target\n"
        )
        with open(service_file, "w") as f:
            for content in service_contents:
                f.write(content)

        # Equivalent of chmod 644 on the service file.
        st = os.stat(service_file)
        os.chmod(
            service_file,
            st.st_mode |
            stat.S_IRUSR |
            stat.S_IWUSR |
            stat.S_IRGRP |
            stat.S_IWGRP |
            stat.S_IROTH
        )

        # Equivalent of chmod 744 on the boot file.
        st = os.stat(boot_file)
        os.chmod(
            boot_file,
            st.st_mode |
            stat.S_IRUSR |
            stat.S_IWUSR |
            stat.S_IXUSR |
            stat.S_IRGRP |
            stat.S_IWGRP |
            stat.S_IXGRP |
            stat.S_IROTH
        )

        filename = service_path + service_file
        cmd_copy = f"cp {service_file} {filename}"
        os.system(cmd_copy)

        args = [
            "systemctl daemon-reload",
            f"systemctl enable {service_file}",
            f"systemctl start {service_file}"
        ]

        for arg in args:
            try:
                subprocess.check_output(arg, shell=True)
            except subprocess.CalledProcessError as e:
                print(e)
    print("$ Completed debuff install")


if __name__ == "__main__":
    apt_update()
    install_pip()
    install_networking()
    install_requirements()
    install_debuff()
