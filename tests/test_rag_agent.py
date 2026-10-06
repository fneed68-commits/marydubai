# tests/test_rag_agent.py
"""اختبارات وكيل RAG"""
import unittest
import os
import tempfile
from unittest.mock import patch
from rag_time_manager_agent import RAGTimeManagerAgent


class TestRAGAgent(unittest.TestCase):

    def setUp(self):
        # قاعدة بيانات مؤقتة لكل اختبار
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        self.agent = RAGTimeManagerAgent(
            db_path=self.tmp_db,
            use_local_embedder=True
        )

    def tearDown(self):
        if os.path.exists(self.tmp_db):
            os.remove(self.tmp_db)

    def test_init_empty(self):
        """الوكيل يبدأ بقاعدة فارغة"""
        self.assertEqual(self.agent.store.count(), 0)

    def test_index_single_chunk(self):
        """فهرسة وثيقة قصيرة = قطعة واحدة"""
        count = self.agent.index_document("نص قصير للاختبار")
        self.assertEqual(count, 1)
        self.assertEqual(self.agent.store.count(), 1)

    def test_index_long_document_multiple_chunks(self):
        """وثيقة طويلة = عدة قطع"""
        long_text = " ".join([f"كلمة{i}" for i in range(1000)])
        count = self.agent.index_document(long_text)
        self.assertGreater(count, 1)
        self.assertEqual(self.agent.store.count(), count)

    def test_index_with_metadata(self):
        """الـ metadata تُخزَّن بشكل صحيح"""
        self.agent.index_document(
            "وثيقة اختبار",
            metadata={"source": "test.md", "type": "test"}
        )
        # البحث
        results = self.agent.store.search(
            self.agent.embedder.embed("اختبار"), k=1
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["metadata"]["source"], "test.md")

    def test_retrieve_empty_index(self):
        """البحث في index فارغ = صفر نتائج"""
        results = self.agent.retrieve_context("أي استعلام")
        self.assertEqual(len(results), 0)

    def test_retrieve_returns_results(self):
        """البحث يعيد نتائج بعد الفهرسة"""
        self.agent.index_document("وثيقة عن الثغرات الأمنية")
        results = self.agent.retrieve_context("ثغرات", k=5)
        self.assertGreater(len(results), 0)
        self.assertIn("score", results[0])
        self.assertIn("text", results[0])
        self.assertIn("metadata", results[0])

    def test_analyze_with_context_empty(self):
        """التحليل بدون بيانات = EMPTY"""
        summary = self.agent.analyze_with_context("سؤال")
        self.assertEqual(summary["status"], "EMPTY")
        self.assertEqual(len(summary["contexts"]), 0)

    def test_analyze_with_context_ok(self):
        """التحليل مع بيانات = OK"""
        self.agent.index_document("وثيقة اختبار مهمة")
        summary = self.agent.analyze_with_context("اختبار")
        self.assertEqual(summary["status"], "OK")
        self.assertGreater(len(summary["contexts"]), 0)
        self.assertIn("query", summary)
        self.assertIn("retrieved_at", summary)

    @patch("builtins.input", return_value="yes")
    def test_captain_approves(self, mock_input):
        """الموجه يوافق على التحليل"""
        self.agent.index_document("وثيقة اختبار")
        summary = self.agent.analyze_with_context("اختبار")
        approved = self.agent.await_captain_command(summary)
        self.assertTrue(approved)

    @patch("builtins.input", return_value="no")
    def test_captain_rejects(self, mock_input):
        """الموجه يرفض التحليل"""
        self.agent.index_document("وثيقة اختبار")
        summary = self.agent.analyze_with_context("اختبار")
        approved = self.agent.await_captain_command(summary)
        self.assertFalse(approved)

    def test_log_decision(self):
        """تسجيل القرارات يعمل"""
        entry = self.agent.log_decision("approved", [1, 2, 3], "ملاحظة")
        self.assertEqual(entry["decision"], "approved")
        self.assertEqual(entry["context_ids"], [1, 2, 3])
        self.assertEqual(entry["notes"], "ملاحظة")
        self.assertIn("timestamp", entry)

    def test_session_summary(self):
        """ملخص الجلسة يحتوي على الحقول المتوقعة"""
        self.agent.index_document("وثيقة")
        self.agent.log_decision("test", [0])
        summary = self.agent.get_session_summary()
        self.assertEqual(summary["agent"], "MaryDubai-RAGTimeManager")
        self.assertEqual(summary["decisions_count"], 1)
        self.assertEqual(summary["total_indexed"], 1)

    def test_chunk_empty_text(self):
        """النص الفارغ لا يُنتج قطعاً"""
        chunks = self.agent._chunk_text("")
        # قد يعيد [""] (نص فارغ واحد)
        self.assertLessEqual(len(chunks), 1)

    def test_chunk_short_text(self):
        """النص القصير = قطعة واحدة"""
        chunks = self.agent._chunk_text("نص قصير")
        self.assertEqual(len(chunks), 1)


if __name__ == "__main__":
    unittest.main()
