# tests/test_temporal_agent.py
"""اختبارات الوكيل الزمني"""
import unittest
from unittest.mock import patch
from temporal_edge_agent import TemporalEdgeAgent


class TestTemporalAgent(unittest.TestCase):

    def setUp(self):
        self.agent = TemporalEdgeAgent()

    def test_proven_record(self):
        """الرقم القياسي مثبّت بشكل صحيح"""
        self.assertEqual(self.agent.proven_record_time, 1.336)

    def test_time_above_threshold(self):
        """وقت أعلى من الحد = آمن"""
        result = self.agent.test_lower_time_limit(1.5)
        self.assertTrue(result)

    def test_time_below_threshold(self):
        """وقت أقل من الحد = خطر"""
        result = self.agent.test_lower_time_limit(1.1)
        self.assertFalse(result)

    def test_time_exact_threshold(self):
        """وقت = الحد بالضبط = آمن"""
        result = self.agent.test_lower_time_limit(1.336)
        self.assertTrue(result)

    def test_time_just_below(self):
        """وقت أقل بقليل = خطر"""
        result = self.agent.test_lower_time_limit(1.3359)
        self.assertFalse(result)

    @patch("builtins.input", return_value="yes")
    def test_captain_accepts_risk(self, mock_input):
        result = self.agent.await_captain_decision("اختبار")
        self.assertTrue(result)

    @patch("builtins.input", return_value="no")
    def test_captain_rejects_risk(self, mock_input):
        result = self.agent.await_captain_decision("اختبار")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
