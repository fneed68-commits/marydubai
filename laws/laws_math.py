#!/usr/bin/env python3
"""
قوانين الرياضيات — القائمة الأساسية
"""
import math
from framework import Law


# ═══════════════════════════════════════════════════════
# 1. مشتقة متعددة الحدود
# ═══════════════════════════════════════════════════════
def derivative_poly(coef, x):
    """مشتقة: a_n*x^n + ... + a_0"""
    n = len(coef) - 1
    return sum(coef[i] * (n - i) * x ** (n - i - 1)
               for i in range(len(coef) - 1))


laws = [
    Law(
        name="مشتقة متعددة الحدود",
        formula="f'(x) لـ f(x) = a*x^n + ... + c",
        func=derivative_poly,
        test_cases=[
            # f(x) = x²  →  f'(x) = 2x
            {"input": ([1, 0, 0], 3), "expected": 6},       # 2*3 = 6
            # f(x) = 2x  →  f'(x) = 2
            {"input": ([2, 0], 5), "expected": 2},
            # f(x) = 5  →  f'(x) = 0
            {"input": ([5], 10), "expected": 0},
            # f(x) = 3x² + 2x + 1  →  f'(x) = 6x + 2
            {"input": ([3, 2, 1], 2), "expected": 14},      # 6*2+2
        ],
    ),

    # ═══════════════════════════════════════════════════
    # 2. قانون أوم
    # ═══════════════════════════════════════════════════
    Law(
        name="قانون أوم",
        formula="V = I × R",
        func=lambda I, R: I * R,
        test_cases=[
            {"input": (2, 10), "expected": 20},
            {"input": (0.5, 100), "expected": 50},
            {"input": (1, 1), "expected": 1},
            {"input": (10, 0), "expected": 0},
        ],
    ),

    # ═══════════════════════════════════════════════════
    # 3. طاقة الحركة
    # ═══════════════════════════════════════════════════
    Law(
        name="طاقة الحركة",
        formula="KE = ½ × m × v²",
        func=lambda m, v: 0.5 * m * v ** 2,
        test_cases=[
            {"input": (2, 3), "expected": 9},        # 0.5 * 2 * 9
            {"input": (1, 1), "expected": 0.5},
            {"input": (10, 0), "expected": 0},
            {"input": (4, 5), "expected": 50},       # 0.5 * 4 * 25
        ],
    ),

    # ═══════════════════════════════════════════════════
    # 4. القاسم المشترك الأكبر
    # ═══════════════════════════════════════════════════
    Law(
        name="القاسم المشترك الأكبر",
        formula="gcd(a, b)",
        func=lambda a, b: math.gcd(a, b) if a >= 0 and b >= 0 else None,
        test_cases=[
            {"input": (48, 18), "expected": 6},
            {"input": (100, 75), "expected": 25},
            {"input": (7, 13), "expected": 1},
            {"input": (0, 5), "expected": 5},
            {"input": (12, 12), "expected": 12},
        ],
    ),

    # ═══════════════════════════════════════════════════
    # 5. اختبار الأولية
    # ═══════════════════════════════════════════════════
    Law(
        name="اختبار الأولية",
        formula="is_prime(n)",
        func=lambda n: (
            n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))
        ),
        test_cases=[
            {"input": (2,), "expected": True},
            {"input": (3,), "expected": True},
            {"input": (4,), "expected": False},
            {"input": (17,), "expected": True},
            {"input": (97,), "expected": True},
            {"input": (100,), "expected": False},
            {"input": (1,), "expected": False},
            {"input": (0,), "expected": False},
        ],
    ),

    # ═══════════════════════════════════════════════════
    # 6. المقلوب المعياري (Crypto)
    # ═══════════════════════════════════════════════════
    Law(
        name="المقلوب المعياري",
        formula="a × a⁻¹ ≡ 1 (mod m)",
        func=lambda a, m: pow(a, -1, m) if math.gcd(a, m) == 1 else None,
        test_cases=[
            {"input": (3, 11), "expected": 4},       # 3*4=12 ≡ 1 mod 11
            {"input": (7, 11), "expected": 8},       # 7*8=56 ≡ 1 mod 11
            {"input": (2, 5), "expected": 3},        # 2*3=6 ≡ 1 mod 5
            {"input": (10, 17), "expected": 12},     # 10*12=120 ≡ 1 mod 17
        ],
    ),
]
