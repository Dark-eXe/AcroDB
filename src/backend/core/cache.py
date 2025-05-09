import time

class SessionCache:
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        entry = self.cache.get(key)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            # Expired – remove it and return None
            del self.cache[key]
            return None
        return entry["value"]

    def set(self, key, value):
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + self.ttl
        }

    def clear(self):
        """Optional: clear the whole cache"""
        self.cache.clear()
