#!/usr/bin/env python3
"""
نظام Cache ذكي مع TTL (Time To Live)
يقرب الاستعلامات المتكررة من الصفر
"""
import time
import hashlib
import json
from functools import wraps
from threading import Lock


class SmartCache:
    """Cache في الذاكرة مع TTL وإحصائيات"""
    
    def __init__(self, default_ttl=300):
        self._data = {}
        self._lock = Lock()
        self.default_ttl = default_ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "sets": 0,
        }
    
    def _make_key(self, *args, **kwargs):
        """يحوّل المعاملات إلى مفتاح فريد"""
        content = json.dumps(
            {"args": args, "kwargs": kwargs},
            sort_keys=True,
            default=str,
        )
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, key):
        """يسترجع قيمة — أو None"""
        with self._lock:
            if key not in self._data:
                self.stats["misses"] += 1
                return None
            
            value, expires_at = self._data[key]
            
            if time.time() > expires_at:
                # انتهت الصلاحية
                del self._data[key]
                self.stats["evictions"] += 1
                self.stats["misses"] += 1
                return None
            
            self.stats["hits"] += 1
            return value
    
    def set(self, key, value, ttl=None):
        """يخزّن قيمة"""
        ttl = ttl or self.default_ttl
        with self._lock:
            self._data[key] = (value, time.time() + ttl)
            self.stats["sets"] += 1
    
    def cached(self, ttl=None):
        """Decorator للتخزين التلقائي"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self._make_key(func.__name__, *args, **kwargs)
                result = self.get(key)
                if result is not None:
                    return result
                result = func(*args, **kwargs)
                self.set(key, result, ttl)
                return result
            return wrapper
        return decorator
    
    def clear(self):
        """مسح كل الـ cache"""
        with self._lock:
            self._data.clear()
    
    def info(self):
        """إحصائيات"""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total * 100 if total else 0
        return {
            "size": len(self._data),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": f"{hit_rate:.1f}%",
            "sets": self.stats["sets"],
            "evictions": self.stats["evictions"],
        }


# نسخة عالمية للاستخدام في المشروع
_global_cache = SmartCache(default_ttl=300)


def cached(ttl=None):
    """Decorator سريع"""
    return _global_cache.cached(ttl)


def get_global_cache():
    return _global_cache
