#!/usr/bin/env python3
"""اختبار Cache على RAG الحقيقي"""
import time
from rag_time_manager_agent import RAGTimeManagerAgent

agent = RAGTimeManagerAgent(
    db_path="./rag_index.db",
    use_local_embedder=False
)

print("=" * 60)
print("🧪 اختبار Cache على RAG الفعلي")
print("=" * 60)

queries = [
    "ما هي الميزات؟",
    "كم عدد الوكلاء؟",
    "كيف يعمل HITL؟",
    "ما هي الميزات؟",
    "كم عدد الوكلاء؟",
    "كيف يعمل HITL؟",
]

print(f"\n📊 {len(queries)} استعلام (3 جديدة + 3 مكررة)\n")

# المرة الأولى
print("─" * 60)
print("🔍 المرة الأولى — بحث حقيقي")
print("─" * 60)

t1_start = time.time()
for q in queries:
    agent.retrieve_context(q, k=3)
t1 = time.time() - t1_start
print(f"\n⏱️  الوقت: {t1*1000:.0f} ms")

# المرة الثانية (cache)
print()
print("─" * 60)
print("⚡ المرة الثانية — من Cache")
print("─" * 60)

t2_start = time.time()
for q in queries:
    agent.retrieve_context(q, k=3)
t2 = time.time() - t2_start
print(f"\n⏱️  الوقت: {t2*1000:.2f} ms")

print()
print("=" * 60)
if t2 > 0:
    print(f"📊 التحسن: {t1/t2:.0f}x أسرع")
print()
print("📊 إحصائيات Cache:")
for k, v in agent.cache_info().items():
    print(f"   {k}: {v}")
print("=" * 60)
