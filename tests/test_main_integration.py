# tests/test_main_integration.py
"""اختبارات تكامل main.py"""
import unittest
import subprocess
import os


class TestMainIntegration(unittest.TestCase):

    def _run(self, *args, input_text=""):
        """تشغيل main.py مع args"""
        result = subprocess.run(
            ["python3", "main.py", *args],
            capture_output=True,
            text=True,
            input=input_text,
            timeout=30,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return result

    def test_list_command(self):
        """--list يعمل"""
        result = self._run("--list")
        self.assertEqual(result.returncode, 0)
        self.assertIn("rag", result.stdout)
        self.assertIn("legal", result.stdout)

    def test_no_args_shows_help(self):
        """بدون args = عرض القائمة"""
        result = self._run()
        self.assertEqual(result.returncode, 0)
        self.assertIn("MaryDubai", result.stdout)

    def test_unknown_agent(self):
        """وكيل غير معروف = خطأ"""
        result = self._run("--agent", "unknown_agent")
        self.assertNotEqual(result.returncode, 0)

    def test_rag_query_local(self):
        """بحث RAG محلي"""
        result = self._run(
            "--agent", "rag",
            "--query", "اختبار",
            input_text="yes\n"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("RAGTimeManager", result.stdout)

    def test_legal_action(self):
        """إجراء قانوني"""
        result = self._run(
            "--agent", "legal",
            "--action", "تقرير اختبار",
            input_text="yes\n"
        )
        self.assertEqual(result.returncode, 0)

    def test_temporal_safe_time(self):
        """وقت آمن"""
        result = self._run(
            "--agent", "temporal",
            "--time", "1.5",
            input_text=""
        )
        self.assertEqual(result.returncode, 0)

    def test_temporal_dangerous_time(self):
        """وقت خطر يستدعي HITL"""
        result = self._run(
            "--agent", "temporal",
            "--time", "1.1",
            input_text="no\n"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("تجميد", result.stdout)


if __name__ == "__main__":
    unittest.main()
