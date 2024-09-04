import socket
import psutil  #type:ignore

def get_local_ip() -> str:
    """
    Gets the local ip on a windows computer.

    :return: The ip.
    """
    return [addr.address for addr in psutil.net_if_addrs().get('Ethernet', []) if addr.family == socket.AF_INET][0]