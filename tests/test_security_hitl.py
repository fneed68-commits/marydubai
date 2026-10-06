# tests/test_security_hitl.py
"""
اختبارات الأمان - محاولات تجاوز HITL
الهدف: التأكد من أن النظام لا ينفذ بدون تصريح بشري صريح
"""
import unittest
from unittest.mock import patch
from legal_consultant_agent import LegalConsultantAgent
from loop_breaker_agent import LoopBreakerAgent
from temporal_edge_agent import TemporalEdgeAgent


class TestHITLBypass(unittest.TestCase):
    """محاولات تجاوز بوابة HITL بمدخلات مختلفة"""

    def setUp(self):
        self.legal = LegalConsultantAgent()
        self.loop = LoopBreakerAgent()
        self.temporal = TemporalEdgeAgent()

    # === محاولات قبول خاطئة (يجب أن ترفض) ===

    @patch("builtins.input", return_value="y")
    def test_short_y_rejected(self, mock_input):
        """y وحدها = رفض (يجب 'yes' كاملة)"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="yes please")
    def test_extra_text_rejected(self, mock_input):
        """yes مع نص إضافي = رفض (لأننا نطلب تطابق تام)"""
        result = self.legal.await_human_command("إجراء")
        # ملاحظة: الكود الحالي يستخدم 'yes' كاملة بعد strip و lower
        # 'yes please' سترفض
        self.assertFalse(result)

    @patch("builtins.input", return_value="1")
    def test_number_rejected(self, mock_input):
        """رقم = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="true")
    def test_true_rejected(self, mock_input):
        """true = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="ok")
    def test_ok_rejected(self, mock_input):
        """ok = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    # === محاولات حقن أوامر (يجب أن ترفض) ===

    @patch("builtins.input", return_value="yes; rm -rf /")
    def test_command_injection_rejected(self, mock_input):
        """حقن أوامر = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="yes\x00no")
    def test_null_byte_rejected(self, mock_input):
        """null byte = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="YES\x00")
    def test_null_after_yes_rejected(self, mock_input):
        """null بعد YES = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    # === محاولات Unicode خبيثة (يجب أن ترفض) ===

    @patch("builtins.input", return_value="уes")  # у = Cyrillic
    def test_cyrillic_y_rejected(self, mock_input):
        """حرف سيريلي = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    @patch("builtins.input", return_value="yeｓ")  # ｓ = fullwidth
    def test_fullwidth_s_rejected(self, mock_input):
        """حرف fullwidth = رفض"""
        result = self.legal.await_human_command("إجراء")
        self.assertFalse(result)

    # === حالات مقبولة (يجب أن توافق) ===

    @patch("builtins.input", return_value="yes")
    def test_plain_yes_accepted(self, mock_input):
        """yes بسيطة = موافقة"""
        result = self.legal.await_human_command("إجراء")
        self.assertTrue(result)

    @patch("builtins.input", return_value="YES")
    def test_uppercase_yes_accepted(self, mock_input):
        """YES كبيرة = موافقة"""
        result = self.legal.await_human_command("إجراء")
        self.assertTrue(result)

    @patch("builtins.input", return_value="  yes  ")
    def test_padded_yes_accepted(self, mock_input):
        """yes مع مسافات = موافقة"""
        result = self.legal.await_human_command("إجراء")
        self.assertTrue(result)

    @patch("builtins.input", return_value="YeS")
    def test_mixed_case_yes_accepted(self, mock_input):
        """YeS مختلطة = موافقة"""
        result = self.legal.await_human_command("إجراء")
        self.assertTrue(result)

    # === اختبار إضافي: مدخلات طويلة جداً ===

    @patch("builtins.input", return_value="yes" + " " * 10000)
    def test_very_long_input_accepted_after_strip(self, mock_input):
        """yes + مسافات كثيرة = موافقة"""
        result = self.legal.await_human_command("إجراء")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
