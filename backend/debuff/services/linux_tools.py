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


def build_details(cmd_input, cmd_output, error_msg, is_errored):
    details = {
        "command_input": cmd_input,
        "command_output": cmd_output,
        "error_message": error_msg,
        "is_errored": is_errored
    }
    return details


def error_handling(cmd_input: str):
    try:
        return subprocess.check_output(cmd_input, shell=True)
    except subprocess.CalledProcessError as e:
        return e


def ip_addr_show_dev(interface: str):
    cmd_input = f"ip -j addr show dev {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False 

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:    
        cmd_output = json.loads(cmd_output)[0]
    
    details = build_details(cmd_input, cmd_output, error_msg, is_errored)
 
    return details


def ethtool_check_ring_buffers(interface: str):
    cmd_input = f"ethtool -g {interface}"
    cmd_output = error_handling(cmd_input)
    error_msg = None
    is_errored = False 

    if isinstance(cmd_output, Exception):
        error_msg = cmd_output
        cmd_output = None
        is_errored = True
    else:
        new_dict = {}
        suffix = "_ring_max"

        cmd_output = cmd_output.decode().split("\n")

        for line in cmd_output:
            line = line.lower()
            line = line.replace(":", "")
            line = line.replace(" ", "_")
            line = re.split("\t+", line)
            
            if "current" in line[0]:
                suffix = "_ring_set"

            if len(line) == 2:
                key = line[0] + suffix 
                value = int(line[1])
                new_dict[key] = value

        cmd_output = new_dict
    
    details = build_details(cmd_input, cmd_output, error_msg, is_errored)
    
    return details


if __name__ == '__main__':
    print(ip_link_show_dev("enp2s0"))
    print(ethtool_check_ring_buffers("enp2s0"))
