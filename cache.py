import hashlib
import json
import logging

try:
    import redis
except ImportError:
    redis = None

from config import REDIS_URL

class SimpleCache:
    """Lightweight caching. Works with local Redis, cloud Redis, or gracefully skips if unavailable."""
    def __init__(self):
        self.client = None
        if REDIS_URL and redis:
            try:
                self.client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=1)
                self.client.ping()
            except Exception:
                logging.warning("Redis unavailable. Cache layer running in bypass mode.")
                self.client = None

    def _hash_key(self, prompt: str) -> str:
        return "nexus_cache:" + hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str):
        if not self.client:
            return None
        try:
            key = self._hash_key(prompt)
            cached = self.client.get(key)
            return json.loads(cached) if cached else None
        except Exception:
            return None

    def set(self, prompt: str, response_data: dict, ttl: int = 3600):
        if not self.client:
            return
        try:
            key = self._hash_key(prompt)
            self.client.setex(key, ttl, json.dumps(response_data))
        except Exception:
            pass

cache = SimpleCache()