import subprocess


def get_list_of_interfaces() -> list:
    interfaces = subprocess.run(["ls", "/sys/class/net"], capture_output=True)
    result = interfaces.stdout.decode().splitlines()
    result.remove('lo')
    return result


def tcshow(interface: str):
    result = subprocess.run(["tcshow", interface], capture_output=True)
    result = result.stdout.decode()
    return result



