#!/usr/bin/env python3
"""
Index Builder - بناء قاعدة معرفة للـ RAG
مع دعم Rate Limit لـ Gemini
"""
import argparse
import time
from pathlib import Path
from shared.embeddings import GeminiEmbedder, LocalHashEmbedder
from shared.vector_store import SQLiteVectorStore


SUPPORTED_EXTENSIONS = {".md", ".txt", ".py", ".json", ".html"}


def main():
    parser = argparse.ArgumentParser(description="MaryDubai RAG Index Builder")
    parser.add_argument("--source", required=True, help="مجلد أو ملف")
    parser.add_argument("--db", default="./rag_index.db", help="مسار قاعدة البيانات")
    parser.add_argument("--clear", action="store_true", help="حذف الـ Index الحالي")
    parser.add_argument("--local", action="store_true", help="استخدم embedder محلي")
    parser.add_argument("--chunk-size", type=int, default=400)
    parser.add_argument("--delay", type=float, default=1.2, help="تأخير بين القطع (ثواني)")
    args = parser.parse_args()

    embedder = LocalHashEmbedder() if args.local else GeminiEmbedder()
    embedder_name = "LOCAL" if args.local else "GEMINI"
    store = SQLiteVectorStore(args.db)

    print(f"🚀 MaryDubai Index Builder")
    print(f"   Embedder: {embedder_name}")
    print(f"   Index: {args.db}")
    print(f"   Delay: {args.delay}s per chunk")

    if args.clear:
        print("🗑️ حذف الـ Index الحالي...")
        store.clear()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"❌ المسار غير موجود: {source_path}")
        return

    if source_path.is_file():
        files = [source_path]
    else:
        files = []
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(source_path.rglob(f"*{ext}"))

    # استثناءات
    files = [f for f in files if not any(
        p in str(f) for p in ["__pycache__", ".git", "node_modules", 
                              "shared/", "receipts/", "backup", ".backup"]
    )]

    print(f"\n📂 وجدت {len(files)} ملف")

    total_chunks = 0
    failed_chunks = 0

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"⚠️ تعذّر قراءة {file_path}: {e}")
            continue

        words = content.split()
        chunk_size = args.chunk_size
        overlap = 50
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 30:
                chunks.append((i // (chunk_size - overlap), chunk))

        print(f"\n📄 {file_path.name} ({len(chunks)} قطعة)")

        for chunk_idx, chunk_text in chunks:
            try:
                embedding = embedder.embed(chunk_text)
                store.add(chunk_text, embedding, {
                    "source": str(file_path),
                    "filename": file_path.name,
                    "chunk_index": chunk_idx
                })
                total_chunks += 1
                print(f"   ✓ قطعة {chunk_idx}")
                
                # تأخير بين القطع
                if not args.local:
                    time.sleep(args.delay)
                    
            except Exception as e:
                failed_chunks += 1
                print(f"   ⚠️ فشل: {str(e)[:100]}")
                
                # إذا فشل بسبب Rate Limit، انتظر أكثر
                if "429" in str(e) or "Rate limit" in str(e):
                    print(f"   ⏳ انتظار 30s قبل المتابعة...")
                    time.sleep(30)

    print(f"\n{'=' * 60}")
    print(f"✅ اكتمل الفهرسة")
    print(f"   📊 المجموع الكلي: {store.count()} قطعة")
    print(f"   📥 المضافة حديثاً: {total_chunks}")
    if failed_chunks > 0:
        print(f"   ⚠️ فشل: {failed_chunks} قطعة (أعد البناء لاحقاً)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
