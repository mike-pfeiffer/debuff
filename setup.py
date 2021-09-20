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

import sys
import platform
import lsb_release


def validate_os():
    """Exits script if invalid OS detected for Debuff install."""

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


if __name__ == '__main__':
    validate_os()
