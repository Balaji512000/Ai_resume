import json
import os

CACHE_FILE = "local_query_cache.json"

class ResponseCache:
    """Manages local JSON cache for repeated questions."""
    
    @staticmethod
    def get(query: str):
        if not os.path.exists(CACHE_FILE):
            return None
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
                return cache.get(query.lower().strip())
        except Exception:
            return None

    @staticmethod
    def set(query: str, response: str):
        cache = {}
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except Exception:
                pass
        cache[query.lower().strip()] = response
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=4)
        except Exception:
            pass

    @staticmethod
    def clear():
        if os.path.exists(CACHE_FILE):
            try:
                os.remove(CACHE_FILE)
            except Exception:
                pass
