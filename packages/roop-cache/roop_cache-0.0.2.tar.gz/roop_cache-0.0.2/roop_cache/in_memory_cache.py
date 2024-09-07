import threading
# this is used to ensure that the instance creation is thread-safe.
class Cache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'cache'):
            self.cache = {}

    def get(self, key):
        """Retrieve an item from the cache."""
        return self.cache.get(key)

    def set(self, key, value):
        """Set an item in the cache."""
        self.cache[key] = value
