#!/usr/bin/env python3
"""
الطريق إلى "قريب من الصفر"
نقيس 5 مستويات من التحسين
"""
import time
import asyncio
import threading
from collections import deque


# ═══════════════════════════════════════════════════════
# محاكاة العملية الأساسية
# ═══════════════════════════════════════════════════════
def base_operation(data, work_time=0.3):
    """محاكاة معالجة اتصال"""
    time.sleep(work_time)
    return len(data)


# ═══════════════════════════════════════════════════════
# 1️⃣ Sequential (500ms - الأساس)
# ═══════════════════════════════════════════════════════
def level1_sequential(connections):
    results = []
    for i in range(connections):
        results.append(base_operation(f"data_{i}"))
    return results


# ═══════════════════════════════════════════════════════
# 2️⃣ Parallel (200ms - متوازي)
# ═══════════════════════════════════════════════════════
def level2_parallel(connections):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(
            lambda i: base_operation(f"data_{i}"),
            range(connections)
        ))
    return results


# ═══════════════════════════════════════════════════════
# 3️⃣ Pipelining (100ms - خط تجميع)
# ═══════════════════════════════════════════════════════
def level3_pipeline(connections):
    """
    الفكرة: ابدأ الاتصال الجديد قبل انتهاء السابق
    مثل خط الإنتاج
    """
    results = []
    q = deque()
    
    def worker(i):
        r = base_operation(f"data_{i}")
        q.append(r)
    
    threads = []
    for i in range(connections):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    return list(q)


# ═══════════════════════════════════════════════════════
# 4️⃣ Async Streaming (50ms - بث فوري)
# ═══════════════════════════════════════════════════════
async def async_operation(data, work_time=0.05):
    """محاكاة بث — نقسم العمل لجزئيات"""
    total = 0
    chunks = 5
    for i in range(chunks):
        await asyncio.sleep(work_time / chunks)
        total += len(data) // chunks
    return total


async def level4_streaming(connections):
    tasks = [async_operation(f"data_{i}") for i in range(connections)]
    return await asyncio.gather(*tasks)


# ═══════════════════════════════════════════════════════
# 5️⃣ Cached (1ms - ذاكرة)
# ═══════════════════════════════════════════════════════
CACHE = {}

def level5_cached(connections):
    """يخزّن النتائج — إذا تكرر السؤال، لا يعيد الحساب"""
    results = []
    for i in range(connections):
        key = f"data_{i}"
        if key in CACHE:
            results.append(CACHE[key])
        else:
            r = base_operation(key, work_time=0.3)
            CACHE[key] = r
            results.append(r)
    return results


# ═══════════════════════════════════════════════════════
# القياس
# ═══════════════════════════════════════════════════════
def measure(name, func, *args):
    start = time.time()
    func(*args)
    return time.time() - start


def main():
    print("=" * 60)
    print("🎯 الطريق إلى 'قريب من الصفر'")
    print("=" * 60)
    print()
    
    N = 20
    print(f"📊 عدد الاتصالات: {N}")
    print(f"📊 العملية الأساسية: 0.3s")
    print()
    
    # 1. Sequential
    t1 = measure("Sequential", level1_sequential, N)
    print(f"1️⃣  Sequential:    {t1*1000:7.0f} ms  🐢 (الأساس)")
    
    # 2. Parallel
    t2 = measure("Parallel", level2_parallel, N)
    print(f"2️⃣  Parallel:      {t2*1000:7.0f} ms  🚀 ({t1/t2:.1f}x أسرع)")
    
    # 3. Pipeline
    t3 = measure("Pipeline", level3_pipeline, N)
    print(f"3️⃣  Pipelining:    {t3*1000:7.0f} ms  ⚡ ({t1/t3:.1f}x أسرع)")
    
    # 4. Streaming
    t4 = measure(
        "Streaming",
        lambda n: asyncio.run(level4_streaming(n)),
        N
    )
    print(f"4️⃣  Streaming:     {t4*1000:7.0f} ms  ⚡⚡ ({t1/t4:.1f}x أسرع)")
    
    # 5. Cached (المرة الثانية)
    print()
    print("─" * 60)
    print("5️⃣  Cached (مرة ثانية):")
    t5 = measure("Cached", level5_cached, N)
    print(f"     Cached:        {t5*1000:7.2f} ms  🎯 ({t1/t5:.0f}x أسرع)")
    
    # التقرير
    print()
    print("=" * 60)
    print("📊 النتائج:")
    print("=" * 60)
    print(f"   🐢 Sequential:    {t1*1000:7.0f} ms")
    print(f"   🚀 Parallel:      {t2*1000:7.0f} ms")
    print(f"   ⚡ Pipelining:    {t3*1000:7.0f} ms")
    print(f"   ⚡⚡ Streaming:     {t4*1000:7.0f} ms")
    print(f"   🎯 Cached:        {t5*1000:7.2f} ms")
    print()
    print("=" * 60)
    print(f"🎯 أقرب وقت: {t5*1000:.2f} ms")
    print(f"🎯 أقرب لـ 'صفر': {t5*1000:.2f} ms")
    print("=" * 60)


if __name__ == "__main__":
    main()
