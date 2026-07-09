import struct
import random

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    s = sum(struct.unpack("!%dH" % (len(data)//2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def generate_random_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def load_useragents():
    # Fallback list
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]

def banner():
    pass