#!/usr/bin/env python3
"""قوانين هندسية (كهربائية + ميكانيكية)"""
import math
from framework import Law


laws = [
    # 1. قانون أوم
    Law(
        name="V = I·R",
        formula="V = I × R",
        func=lambda I, R: I * R,
        test_cases=[
            {"input": (2, 10), "expected": 20},
            {"input": (0.5, 100), "expected": 50},
        ],
    ),

    # 2. القدرة الكهربائية
    Law(
        name="P = V·I",
        formula="P = V × I",
        func=lambda V, I: V * I,
        test_cases=[
            {"input": (12, 2), "expected": 24},
            {"input": (220, 5), "expected": 1100},
        ],
    ),

    # 3. المقاومات على التسلسل
    Law(
        name="مقاومات تسلسل",
        formula="R_total = R1 + R2 + ...",
        func=lambda *R: sum(R),
        test_cases=[
            {"input": (100, 200), "expected": 300},
            {"input": (10, 20, 30), "expected": 60},
            {"input": (1,), "expected": 1},
        ],
    ),

    # 4. المقاومات على التوازي
    Law(
        name="مقاومات توازي",
        formula="1/R = 1/R1 + 1/R2 + ...",
        func=lambda *R: 1 / sum(1 / r for r in R),
        test_cases=[
            {"input": (100, 100), "expected": 50.0},
            {"input": (100, 200), "expected": 200/3},
            {"input": (10, 10, 10), "expected": 10/3},
        ],
    ),

    # 5. RMS
    Law(
        name="V_rms",
        formula="V_rms = V_peak / √2",
        func=lambda Vp: Vp / math.sqrt(2),
        test_cases=[
            {"input": (math.sqrt(2),), "expected": 1.0},
            {"input": (311,), "expected": 311 / math.sqrt(2)},
        ],
    ),

    # 6. الإجهاد
    Law(
        name="الإجهاد",
        formula="σ = F/A",
        func=lambda F, A: F / A if A != 0 else 0,
        test_cases=[
            {"input": (100, 10), "expected": 10.0},
            {"input": (1000, 100), "expected": 10.0},
        ],
    ),

    # 7. الانفعال
    Law(
        name="الانفعال",
        formula="ε = ΔL / L₀",
        func=lambda dL, L: dL / L if L != 0 else 0,
        test_cases=[
            {"input": (1, 100), "expected": 0.01},
            {"input": (5, 50), "expected": 0.1},
        ],
    ),

    # 8. معامل يونغ
    Law(
        name="معامل يونغ",
        formula="E = σ/ε",
        func=lambda sigma, epsilon: sigma / epsilon if epsilon != 0 else 0,
        test_cases=[
            {"input": (100, 0.01), "expected": 10000},
            {"input": (200, 0.02), "expected": 10000},
        ],
    ),
]
