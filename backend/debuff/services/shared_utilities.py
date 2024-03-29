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


def error_response(cmd_input, cmd_output, errors):
    response = {
        "cmd_input": cmd_input,
        "cmd_output": cmd_output,
        "errors": errors
    }
    return response


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
