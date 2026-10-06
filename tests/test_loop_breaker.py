# tests/test_loop_breaker.py
"""اختبارات وكيل كسر الحلقات"""
import unittest
from unittest.mock import patch
from loop_breaker_agent import LoopBreakerAgent


class TestLoopBreaker(unittest.TestCase):

    def setUp(self):
        self.agent = LoopBreakerAgent()

    def test_init_thresholds(self):
        """العتبات مثبّتة بشكل صحيح"""
        self.assertEqual(self.agent.ram_warning_threshold, 70.0)
        self.assertEqual(self.agent.ram_safe_threshold, 67.0)

    def test_first_call_no_break(self):
        """الاستدعاء الأول لا يكسر"""
        result = self.agent.should_break_loop("خطوة", "نتيجة")
        self.assertFalse(result)

    def test_second_call_breaks(self):
        """التكرار الثاني يكسر الحلقة"""
        self.agent.should_break_loop("خطوة", "نتيجة")
        result = self.agent.should_break_loop("خطوة", "نتيجة")
        self.assertTrue(result)

    def test_different_results_no_break(self):
        """نتائج مختلفة لا تكسر"""
        self.agent.should_break_loop("خطوة", "نتيجة1")
        result = self.agent.should_break_loop("خطوة", "نتيجة2")
        self.assertFalse(result)

    def test_whitespace_trimmed(self):
        """المسافات الزائدة تُعالج"""
        self.agent.should_break_loop("خطوة ", " نتيجة ")
        result = self.agent.should_break_loop("  خطوة", "نتيجة  ")
        self.assertTrue(result)

    def test_ram_yellow(self):
        """RAM > 70% = أصفر"""
        result = self.agent.monitor_resources(75.0)
        self.assertEqual(result, "YELLOW")

    def test_ram_green(self):
        """RAM < 67% = أخضر"""
        result = self.agent.monitor_resources(50.0)
        self.assertEqual(result, "GREEN")

    def test_ram_neutral(self):
        """RAM بين 67-70 = حيادي"""
        result = self.agent.monitor_resources(68.5)
        self.assertEqual(result, "NEUTRAL")

    def test_ram_exact_warning(self):
        """RAM = 70 بالضبط = أصفر"""
        result = self.agent.monitor_resources(70.0)
        self.assertEqual(result, "YELLOW")

    def test_ram_exact_safe(self):
        """RAM = 67 بالضبط = أخضر"""
        result = self.agent.monitor_resources(67.0)
        self.assertEqual(result, "GREEN")

    @patch("builtins.input", return_value="yes")
    def test_director_approves(self, mock_input):
        result = self.agent.await_director_command("حالة")
        self.assertTrue(result)

    @patch("builtins.input", return_value="no")
    def test_director_rejects(self, mock_input):
        result = self.agent.await_director_command("حالة")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
