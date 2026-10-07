# rag_time_manager_agent.py
"""
MaryDubai-RAGTimeManager
وكيل RAG حقيقي: يبني قاعدة معرفة، يسترجع السياق، ويتوقف للمراجعة البشرية
"""
import os
from datetime import datetime
from shared.embeddings import GeminiEmbedder, LocalHashEmbedder
from shared.vector_store import SQLiteVectorStore


class RAGTimeManagerAgent:
    def __init__(self, db_path="./rag_index.db", use_local_embedder=False):
        self.agent_name = "MaryDubai-RAGTimeManager"
        self.db_path = db_path
        self.embedder = LocalHashEmbedder() if use_local_embedder else GeminiEmbedder()
        self.embedder_mode = "LOCAL" if use_local_embedder else "GEMINI"
        self.store = SQLiteVectorStore(db_path)
        self.session_log = []
        self.max_context_items = 5

        print(f"✅ [{self.agent_name}] تهيئة الوكيل")
        print(f"   📊 Embedder: {self.embedder_mode}")
        print(f"   💾 Index: {db_path} ({self.store.count()} قطعة موجودة)")

    def _chunk_text(self, text, chunk_size=400, overlap=50):
        if not text or not text.strip():
            return []
        words = text.split()
        if len(words) <= chunk_size:
            return [text]
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 30:
                chunks.append(chunk)
        return chunks

    def index_document(self, content, metadata=None):
        print(f"\n📥 [{self.agent_name}] فهرسة وثيقة جديدة...")
        chunks = self._chunk_text(content)
        print(f"   📄 {len(chunks)} قطعة بعد التقسيم")
        base_meta = metadata or {}
        indexed_count = 0
        for i, chunk in enumerate(chunks):
            try:
                embedding = self.embedder.embed(chunk)
                meta = {**base_meta, "chunk_index": i, "indexed_at": datetime.now().isoformat()}
                self.store.add(chunk, embedding, meta)
                indexed_count += 1
            except Exception as e:
                print(f"   ⚠️ فشل فهرسة القطعة {i}: {e}")
        print(f"✅ [{self.agent_name}] تمت فهرسة {indexed_count} قطعة")
        return indexed_count

    def retrieve_context(self, query, k=None):
        if k is None:
            k = self.max_context_items
        print(f"\n🔍 [{self.agent_name}] بحث: '{query[:60]}...'")
        try:
            query_embedding = self.embedder.embed(query)
            results = self.store.search(query_embedding, k=k)
            print(f"   ✅ {len(results)} نتيجة")
            return results
        except Exception as e:
            print(f"   ⚠️ فشل البحث: {e}")
            return []

    def analyze_with_context(self, query, k=None):
        contexts = self.retrieve_context(query, k=k)
        if not contexts:
            return {"query": query, "contexts": [], "status": "EMPTY"}
        summary = {
            "query": query,
            "contexts": [
                {
                    "text": c["text"],
                    "preview": c["text"][:200] + ("..." if len(c["text"]) > 200 else ""),
                    "score": c["score"],
                    "metadata": c["metadata"]
                }
                for c in contexts
            ],
            "status": "OK",
            "retrieved_at": datetime.now().isoformat()
        }
        return summary

    def await_captain_command(self, analysis_summary):
        print("\n" + "=" * 60)
        print(f"📢 [{self.agent_name}] تقرير تحليل RAG")
        print(f"📝 السؤال: {analysis_summary.get('query', '')}")
        print(f"📊 السياقات: {len(analysis_summary.get('contexts', []))}")
        print("=" * 60)
        contexts = analysis_summary.get("contexts", [])
        for i, ctx in enumerate(contexts[:3], 1):
            score = ctx.get("score", 0)
            preview = ctx.get("preview", "")
            source = ctx.get("metadata", {}).get("source", "غير معروف")
            print(f"\n[{i}] 🎯 تشابه: {score:.3f}")
            print(f"    📁 المصدر: {source}")
            print(f"    📄 {preview}")
        if len(contexts) > 3:
            print(f"\n   ... و {len(contexts) - 3} نتيجة إضافية")
        print()
        command = input("👤 [الموجه كابتن] هل توافق على تمرير هذا التحليل؟ (yes/no): ")
        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم اعتماد التحليل. جاري المتابعة...")
            return True
        else:
            print("🛑 [أمر التجميد] تم إيقاف العملية بناءً على أمر الموجه.")
            return False

    def log_decision(self, decision, context_ids, notes=""):
        entry = {
            "decision": decision,
            "context_ids": context_ids,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self.session_log.append(entry)
        print(f"📝 [{self.agent_name}] تم تسجيل القرار.")
        return entry

    def get_session_summary(self):
        return {
            "agent": self.agent_name,
            "decisions_count": len(self.session_log),
            "total_indexed": self.store.count(),
            "decisions": self.session_log
        }


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 MaryDubai-RAGTimeManager - اختبار تجريبي")
    print("=" * 60)
    agent = RAGTimeManagerAgent(
        db_path="./test_rag.db",
        use_local_embedder=False
    )
    sample_doc = """
    تقرير أمني - HackerOne CTF 232
    تاريخ الفحص: 2026-10-04
    النطاق: api.example.com

    الثغرات المكتشفة:
    1. SQL Injection (Critical) - في نقطة /api/v2/search
    2. XSS Reflected (High) - في نقطة /profile
    3. IDOR (High) - في نقطة /api/v1/users/{id}

    المكافأة المتوقعة: 500-2000 دولار
    """
    agent.index_document(
        sample_doc,
        metadata={"source": "hackerone_ctf_232.md", "type": "security_report"}
    )
    summary = agent.analyze_with_context("ما هي الثغرات الحرجة؟")
    if summary.get("status") == "OK":
        approved = agent.await_captain_command(summary)
        if approved:
            agent.log_decision("approved_analysis", [c["metadata"].get("chunk_index", 0) for c in summary["contexts"]])
    print("\n📊 ملخص الجلسة:")
    print(f"   {agent.get_session_summary()}")
