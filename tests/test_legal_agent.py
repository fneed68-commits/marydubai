# tests/test_legal_agent.py
"""اختبارات الوكيل القانوني"""
import unittest
from unittest.mock import patch
from legal_consultant_agent import LegalConsultantAgent


class TestLegalAgent(unittest.TestCase):

    def setUp(self):
        self.agent = LegalConsultantAgent()

    def test_init(self):
        """الوكيل يُهيَّأ بشكل صحيح"""
        self.assertEqual(self.agent.agent_name, "MaryDubai-LegalGuard")
        self.assertIn("HackerOne_Policy", self.agent.compliance_frameworks)

    def test_valid_action_passes(self):
        """إجراء نظيف يمر التدقيق"""
        result = self.agent.audit_action_compliance(
            "تقرير عادي",
            {"is_automated_spam": False, "is_original_work": True}
        )
        self.assertTrue(result)

    def test_spam_rejected(self):
        """الإجراء العشوائي يُرفض"""
        result = self.agent.audit_action_compliance(
            "spam",
            {"is_automated_spam": True, "is_original_work": True}
        )
        self.assertFalse(result)

    def test_non_original_rejected(self):
        """العمل غير الأصلي يُرفض"""
        result = self.agent.audit_action_compliance(
            "نسخ",
            {"is_automated_spam": False, "is_original_work": False}
        )
        self.assertFalse(result)

    @patch("builtins.input", return_value="yes")
    def test_human_approves(self, mock_input):
        """الموجه يوافق"""
        result = self.agent.await_human_command("إجراء اختبار")
        self.assertTrue(result)

    @patch("builtins.input", return_value="no")
    def test_human_rejects(self, mock_input):
        """الموجه يرفض"""
        result = self.agent.await_human_command("إجراء اختبار")
        self.assertFalse(result)

    @patch("builtins.input", return_value="")
    def test_human_empty_input(self, mock_input):
        """مدخل فارغ = رفض"""
        result = self.agent.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="YES")
    def test_human_uppercase_yes(self, mock_input):
        """YES بحروف كبيرة = موافقة"""
        result = self.agent.await_human_command("إجراء")
        self.assertTrue(result)

    @patch("builtins.input", return_value="  yes  ")
    def test_human_whitespace_yes(self, mock_input):
        """yes مع مسافات = موافقة"""
        result = self.agent.await_human_command("إجراء")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
