"""
Lightweight Vector Store using SQLite - خفيف جداً يعمل على Termux
"""
import sqlite3
import json
import math


class SQLiteVectorStore:
    """مخزن متجهات خفيف يستخدم SQLite + Cosine Similarity"""
    
    def __init__(self, db_path="./rag_index.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                embedding TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON vectors(created_at)
        """)
        conn.commit()
        conn.close()
    
    def add(self, text, embedding, metadata=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vectors (text, embedding, metadata) VALUES (?, ?, ?)",
            (text, json.dumps(embedding), json.dumps(metadata or {}))
        )
        conn.commit()
        conn.close()
    
    def search(self, query_embedding, k=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, embedding, metadata FROM vectors")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return []
        results = []
        for row_id, text, emb_str, meta_str in rows:
            emb = json.loads(emb_str)
            score = self._cosine_similarity(query_embedding, emb)
            results.append({
                "id": row_id,
                "text": text,
                "score": score,
                "metadata": json.loads(meta_str)
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]
    
    def _cosine_similarity(self, a, b):
        if len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
    
    def count(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vectors")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def clear(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vectors")
        conn.commit()
        conn.close()
