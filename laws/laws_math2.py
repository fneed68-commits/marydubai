#!/usr/bin/env python3
"""قوانين رياضية — الجزء الثاني"""
import math
from framework import Law


def _fib(n):
    """متتالية فيبوناتشي"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


laws = [
    # 1. التكامل المحدد لمتعددة حدود
    Law(
        name="التكامل المحدد لمتعددة حدود",
        formula="∫[a,b] f(x) dx",
        func=lambda coef, a, b: sum(
            coef[i] * (b ** (len(coef) - i) - a ** (len(coef) - i)) / (len(coef) - i)
            for i in range(len(coef))
        ),
        test_cases=[
            # ∫[0,2] x dx = x²/2 | [0,2] = 2
            {"input": ([1, 0], 0, 2), "expected": 2.0},
            # ∫[0,3] 2x dx = x² | [0,3] = 9
            {"input": ([2, 0], 0, 3), "expected": 9.0},
            # ∫[0,1] 1 dx = 1
            {"input": ([1], 0, 1), "expected": 1.0},
        ],
    ),

    # 2. المتوسط
    Law(
        name="المتوسط الحسابي",
        formula="mean = Σx / n",
        func=lambda data: sum(data) / len(data) if data else 0,
        test_cases=[
            {"input": ([1, 2, 3, 4, 5],), "expected": 3.0},
            {"input": ([10, 20],), "expected": 15.0},
            {"input": ([5],), "expected": 5.0},
            {"input": ([0, 0, 0],), "expected": 0.0},
        ],
    ),

    # 3. الوسيط
    Law(
        name="الوسيط (Median)",
        formula="middle value",
        func=lambda data: sorted(data)[len(data) // 2] if len(data) % 2 else (sorted(data)[len(data) // 2 - 1] + sorted(data)[len(data) // 2]) / 2,
        test_cases=[
            {"input": ([1, 2, 3],), "expected": 2},
            {"input": ([1, 2, 3, 4],), "expected": 2.5},
            {"input": ([5],), "expected": 5},
            {"input": ([3, 1, 4, 2, 5],), "expected": 3},
        ],
    ),

    # 4. التباين
    Law(
        name="التباين (Variance)",
        formula="σ² = Σ(x - μ)² / n",
        func=lambda data: sum((x - sum(data) / len(data)) ** 2 for x in data) / len(data) if data else 0,
        test_cases=[
            {"input": ([2, 4, 4, 4, 5, 5, 7, 9],), "expected": 4.0},
            {"input": ([1, 1, 1],), "expected": 0.0},
            {"input": ([0, 10],), "expected": 25.0},
        ],
    ),

    # 5. فيبوناتشي
    Law(
        name="فيبوناتشي",
        formula="F(n) = F(n-1) + F(n-2)",
        func=lambda n: _fib(n),
        test_cases=[
            {"input": (0,), "expected": 0},
            {"input": (1,), "expected": 1},
            {"input": (10,), "expected": 55},
            {"input": (20,), "expected": 6765},
        ],
    ),

    # 6. المضروب (Factorial)
    Law(
        name="المضروب",
        formula="n! = n × (n-1) × ... × 1",
        func=lambda n: math.factorial(n),
        test_cases=[
            {"input": (0,), "expected": 1},
            {"input": (1,), "expected": 1},
            {"input": (5,), "expected": 120},
            {"input": (10,), "expected": 3628800},
        ],
    ),

    # 7. التوافيق (Combinations)
    Law(
        name="التوافيق C(n, k)",
        formula="C(n, k) = n! / (k! × (n-k)!)",
        func=lambda n, k: math.comb(n, k) if 0 <= k <= n else 0,
        test_cases=[
            {"input": (5, 2), "expected": 10},
            {"input": (10, 3), "expected": 120},
            {"input": (5, 0), "expected": 1},
            {"input": (5, 5), "expected": 1},
        ],
    ),

    # 8. لوغاريتم
    Law(
        name="اللوغاريتم الطبيعي",
        formula="ln(e^x) = x",
        func=lambda x: math.log(math.exp(x)),
        test_cases=[
            {"input": (0,), "expected": 0.0},
            {"input": (1,), "expected": 1.0},
            {"input": (5,), "expected": 5.0},
            {"input": (-3,), "expected": -3.0},
        ],
    ),

    # 9. جيب الزاوية
    Law(
        name="جا (sin)",
        formula="sin(π/6) = 0.5",
        func=lambda x: math.sin(x),
        test_cases=[
            {"input": (0,), "expected": 0.0},
            {"input": (math.pi / 6,), "expected": 0.5},
            {"input": (math.pi / 2,), "expected": 1.0},
        ],
    ),

    # 10. المسافة بين نقطتين
    Law(
        name="المسافة الإقليدية",
        formula="d = √((x₂-x₁)² + (y₂-y₁)²)",
        func=lambda x1, y1, x2, y2: math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2),
        test_cases=[
            {"input": (0, 0, 3, 4), "expected": 5.0},
            {"input": (1, 1, 4, 5), "expected": 5.0},
            {"input": (0, 0, 0, 0), "expected": 0.0},
        ],
    ),

    # 11. الأس المعياري
    Law(
        name="الأس المعياري",
        formula="base^exp mod m",
        func=lambda b, e, m: pow(b, e, m),
        test_cases=[
            {"input": (2, 10, 1000), "expected": 24},
            {"input": (3, 4, 10), "expected": 1},
            {"input": (5, 0, 10), "expected": 1},
        ],
    ),

    # 12. دالة أويلر
    Law(
        name="دالة أويلر φ(n)",
        formula="عدد الأعداد الأولية مع n",
        func=lambda n: sum(1 for i in range(1, n + 1) if math.gcd(i, n) == 1),
        test_cases=[
            {"input": (1,), "expected": 1},
            {"input": (10,), "expected": 4},
            {"input": (12,), "expected": 4},
            {"input": (7,), "expected": 6},
        ],
    ),

    # 13. نظرية الباقي الصيني
    Law(
        name="نظرية الباقي الصيني",
        formula="x ≡ r_i (mod m_i)",
        func=lambda rems, mods: next(
            x for x in range(math.prod(mods))
            if all(x % m == r for r, m in zip(rems, mods))
        ),
        test_cases=[
            {"input": ([2, 3, 2], [3, 5, 7]), "expected": 23},
            {"input": ([1, 2], [2, 3]), "expected": 5},
        ],
    ),

    # 14. فيثاغورس
    Law(
        name="نظرية فيثاغورس",
        formula="c = √(a² + b²)",
        func=lambda a, b: math.sqrt(a ** 2 + b ** 2),
        test_cases=[
            {"input": (3, 4), "expected": 5.0},
            {"input": (5, 12), "expected": 13.0},
            {"input": (8, 15), "expected": 17.0},
        ],
    ),

    # 15. القاسم المشترك الأصغر
    Law(
        name="المضاعف المشترك الأصغر",
        formula="lcm(a, b) = |a×b| / gcd(a, b)",
        func=lambda a, b: abs(a * b) // math.gcd(a, b) if a and b else 0,
        test_cases=[
            {"input": (4, 6), "expected": 12},
            {"input": (3, 5), "expected": 15},
            {"input": (12, 18), "expected": 36},
        ],
    ),
]
