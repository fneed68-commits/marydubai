#!/usr/bin/env python3
"""اختبار Cache على RAG الحقيقي"""
import sys
import time
sys.path.insert(0, '/data/data/com.termux/files/home/termux_secops_project')

from shared.cache import SmartCache


# إنشاء cache مع TTL = 5 دقائق
cache = SmartCache(default_ttl=300)


def slow_search(query):
    """محاكاة RAG بطيء (Gemini API)"""
    time.sleep(0.6)  # 600ms
    return f"نتيجة لـ: {query}"


@cache.cached(ttl=300)
def cached_search(query):
    """بحث مع cache"""
    return slow_search(query)


def main():
    print("=" * 60)
    print("🧪 اختبار Cache على RAG")
    print("=" * 60)
    print()
    
    queries = [
        "ما هي الميزات؟",
        "كم عدد الوكلاء؟",
        "كيف يعمل HITL؟",
        "ما هي الميزات؟",       # مكرر
        "كم عدد الوكلاء؟",       # مكرر
        "ما هي الميزات؟",       # مكرر
    ]
    
    print(f"📊 {len(queries)} استعلام (3 جديدة + 3 مكررة)")
    print()
    
    # بدون cache
    print("🐢 بدون Cache:")
    start = time.time()
    for q in queries:
        slow_search(q)
    t_slow = time.time() - start
    print(f"   ⏱️  {t_slow*1000:.0f} ms")
    print()
    
    # مع cache
    print("⚡ مع Cache:")
    start = time.time()
    for q in queries:
        cached_search(q)
    t_fast = time.time() - start
    print(f"   ⏱️  {t_fast*1000:.0f} ms")
    print()
    
    print("=" * 60)
    print(f"📊 التحسن: {t_slow/t_fast:.1f}x أسرع")
    print()
    print("📊 إحصائيات Cache:")
    info = cache.info()
    for k, v in info.items():
        print(f"   {k}: {v}")
    print("=" * 60)


if __name__ == "__main__":
    main()
