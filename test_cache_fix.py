#!/usr/bin/env python3
"""اختبار Cache حقيقي — بعد ملء الذاكرة"""
import time

CACHE = {}

def operation(key, work=0.3):
    """محاكاة عملية"""
    if key in CACHE:
        return CACHE[key]
    time.sleep(work)
    result = len(key)
    CACHE[key] = result
    return result

def test_cached_after_warmup():
    print("=" * 60)
    print("🎯 اختبار Cache الحقيقي")
    print("=" * 60)
    print()
    
    N = 20
    
    # 1. المرة الأولى (ملء الـ cache)
    print("🔄 المرة 1 — ملء الذاكرة...")
    start = time.time()
    for i in range(N):
        operation(f"data_{i}")
    t1 = time.time() - start
    print(f"   ⏱️  {t1*1000:.0f} ms  (ملء {N} عنصر)")
    print()
    
    # 2. المرة الثانية (من الذاكرة)
    print("⚡ المرة 2 — من الذاكرة...")
    start = time.time()
    for i in range(N):
        operation(f"data_{i}")
    t2 = time.time() - start
    print(f"   ⏱️  {t2*1000:.2f} ms  (من cache)")
    print()
    
    # 3. المرة الثالثة
    print("🎯 المرة 3 — من الذاكرة...")
    start = time.time()
    for i in range(N):
        operation(f"data_{i}")
    t3 = time.time() - start
    print(f"   ⏱️  {t3*1000:.2f} ms")
    print()
    
    print("=" * 60)
    print(f"📊 النتائج:")
    print(f"   ملء Cache:      {t1*1000:7.0f} ms")
    print(f"   من Cache:       {t2*1000:7.2f} ms")
    print(f"   تحسّن:          {t1/t2:.0f}x  ← قريب من الصفر!")
    print("=" * 60)


if __name__ == "__main__":
    test_cached_after_warmup()
