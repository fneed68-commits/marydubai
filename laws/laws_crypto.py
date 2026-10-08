#!/usr/bin/env python3
"""قوانين التشفير والعملات"""
import math
from framework import Law


def modinv(a, m):
    """المقلوب المعياري"""
    if math.gcd(a, m) != 1:
        return None
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


laws = [
    # 1. المقلوب المعياري
    Law(
        name="المقلوب المعياري",
        formula="a × a⁻¹ ≡ 1 (mod m)",
        func=modinv,
        test_cases=[
            {"input": (3, 11), "expected": 4},
            {"input": (7, 11), "expected": 8},
            {"input": (10, 17), "expected": 12},
        ],
    ),

    # 2. أويلر φ(n)
    Law(
        name="دالة أويلر",
        formula="φ(n) = عدد الأعداد الأولية مع n",
        func=lambda n: sum(1 for i in range(1, n + 1) if math.gcd(i, n) == 1),
        test_cases=[
            {"input": (10,), "expected": 4},
            {"input": (12,), "expected": 4},
            {"input": (7,), "expected": 6},
        ],
    ),

    # 3. الأس المعياري
    Law(
        name="الأس المعياري",
        formula="b^e mod m",
        func=lambda b, e, m: pow(b, e, m),
        test_cases=[
            {"input": (2, 10, 1000), "expected": 24},
            {"input": (3, 4, 10), "expected": 1},
        ],
    ),

    # 4. CRT
    Law(
        name="نظرية الباقي الصيني",
        formula="x ≡ r_i (mod m_i)",
        func=lambda rems, mods: next(
            (x for x in range(math.prod(mods))
             if all(x % m == r for r, m in zip(rems, mods))),
            None
        ),
        test_cases=[
            {"input": ([2, 3, 2], [3, 5, 7]), "expected": 23},
            {"input": ([1, 2], [2, 3]), "expected": 5},
        ],
    ),

    # 5. اختبار أن العدد أولي (Miller-Rabin مبسط)
    Law(
        name="اختبار الأولية",
        formula="is_prime(n)",
        func=lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1)),
        test_cases=[
            {"input": (2,), "expected": True},
            {"input": (17,), "expected": True},
            {"input": (4,), "expected": False},
            {"input": (97,), "expected": True},
        ],
    ),
]
