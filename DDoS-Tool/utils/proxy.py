import random

def load_proxies(file_path=None):
    if file_path:
        try:
            with open(file_path) as f:
                return [line.strip() for line in f if line.strip()]
        except:
            pass
    return None

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies
    def get(self):
        return random.choice(self.proxies) if self.proxies else None