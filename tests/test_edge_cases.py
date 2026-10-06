# tests/test_edge_cases.py
"""اختبارات الحالات الحدّية"""
import unittest
import os
import tempfile
from unittest.mock import patch
from rag_time_manager_agent import RAGTimeManagerAgent


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        self.agent = RAGTimeManagerAgent(
            db_path=self.tmp_db,
            use_local_embedder=True
        )

    def tearDown(self):
        if os.path.exists(self.tmp_db):
            os.remove(self.tmp_db)

    def test_index_very_short_text(self):
        """نص بكلمة واحدة"""
        count = self.agent.index_document("كلمة")
        # قد يفهرس أو لا، حسب طوله
        self.assertGreaterEqual(count, 0)

    def test_index_only_whitespace(self):
        """نص فارغ من المسافات فقط"""
        count = self.agent.index_document("     \n\n\t\t     ")
        self.assertEqual(count, 0)

    def test_index_empty_string(self):
        """نص فارغ"""
        count = self.agent.index_document("")
        self.assertEqual(count, 0)

    def test_index_very_long_text(self):
        """نص ضخم (100,000 كلمة)"""
        text = " ".join([f"كلمة{i}" for i in range(100000)])
        count = self.agent.index_document(text)
        self.assertGreater(count, 100)

    def test_index_unicode_text(self):
        """نص بأحرف يونيكود متعددة"""
        text = "مرحبا 世界 🌍 Hello Привет こんにちは"
        count = self.agent.index_document(text)
        self.assertGreater(count, 0)

    def test_index_emoji_heavy(self):
        """نص كله إيموجي"""
        text = "🎯 🚀 🔥 💡 ⚡ 🌟 ✨ 🎉"
        count = self.agent.index_document(text)
        self.assertGreaterEqual(count, 0)

    def test_duplicate_indexing(self):
        """فهرسة نفس النص مرتين"""
        text = "نص اختبار"
        count1 = self.agent.index_document(text)
        count2 = self.agent.index_document(text)
        self.assertEqual(count1, count2)
        # كلاهما يُفهرس (لا dedup)
        self.assertEqual(self.agent.store.count(), 2)

    def test_search_with_empty_query(self):
        """بحث باستعلام فارغ"""
        self.agent.index_document("وثيقة")
        results = self.agent.retrieve_context("")
        # يجب ألا ينفجر
        self.assertIsInstance(results, list)

    def test_search_k_larger_than_index(self):
        """k أكبر من عدد القطع"""
        self.agent.index_document("وثيقة واحدة")
        results = self.agent.retrieve_context("بحث", k=100)
        self.assertLessEqual(len(results), 1)

    def test_search_k_zero(self):
        """k = 0"""
        self.agent.index_document("وثيقة")
        results = self.agent.retrieve_context("بحث", k=0)
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
