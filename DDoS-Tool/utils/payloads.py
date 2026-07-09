import struct

def get_http_payload(method="GET", path="/", host="example.com"):
    return f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nConnection: keep-alive\r\n\r\n".encode()

def get_dns_query():
    # Query for google.com type A
    transaction_id = b'\x12\x34'
    flags = b'\x01\x00'
    qdcount = b'\x00\x01'
    ancount = b'\x00\x00'
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'
    header = transaction_id + flags + qdcount + ancount + nscount + arcount
    # google.com encoded: \x06google\x03com\x00
    qname = b'\x06google\x03com\x00'
    qtype = b'\x00\x01'  # A
    qclass = b'\x00\x01'
    return header + qname + qtype + qclass

def get_ntp_request():
    # NTP v4, mode 3 (client)
    li_vi_mode = 0x1b
    return struct.pack('!B', li_vi_mode) + b'\x00'*47