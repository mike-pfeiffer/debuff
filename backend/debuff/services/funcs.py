import subprocess


def get_list_of_interfaces() -> list:
    interfaces = subprocess.run(["ls", "/sys/class/net"], capture_output=True)
    result = interfaces.stdout.decode().splitlines()
    result.remove('lo')

    return result
