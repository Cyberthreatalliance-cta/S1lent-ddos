import socket
import random
import ipaddress

def is_ip(addr):
    try:
        ipaddress.ip_address(addr)
        return True
    except:
        return False

def is_domain(addr):
    return not is_ip(addr)

def resolve_domain(domain):
    return socket.gethostbyname(domain)

def check_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def random_bytes(length):
    return bytes(random.randint(0,255) for _ in range(length))

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def get_gateway():
    # dummy
    return "192.168.1.1"

def arp_spoof(target_ip, gateway_ip):
    pass