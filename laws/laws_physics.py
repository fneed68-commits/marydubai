#!/usr/bin/env python3
"""قوانين الفيزياء"""
import math
from framework import Law

C = 299_792_458
H = 6.62607015e-34
G = 6.67430e-11
K_B = 1.380649e-23
E_CHARGE = 1.602176634e-19
G_STD = 9.80665
R_GAS = 8.314462618


laws = [
    # 1. قانون نيوتن الثاني
    Law(
        name="F = m·a",
        formula="F = m × a",
        func=lambda m, a: m * a,
        test_cases=[
            {"input": (10, 9.8), "expected": 98.0},
            {"input": (1, 1), "expected": 1},
            {"input": (5, 20), "expected": 100},
        ],
    ),

    # 2. طاقة الحركة
    Law(
        name="KE = ½mv²",
        formula="KE = ½ × m × v²",
        func=lambda m, v: 0.5 * m * v ** 2,
        test_cases=[
            {"input": (2, 3), "expected": 9.0},
            {"input": (1, 10), "expected": 50.0},
        ],
    ),

    # 3. طاقة الوضع
    Law(
        name="PE = mgh",
        formula="PE = m × g × h",
        func=lambda m, h: m * G_STD * h,
        test_cases=[
            {"input": (1, 10), "expected": 98.0665},
            {"input": (10, 1), "expected": 98.0665},
        ],
    ),

    # 4. E = mc²
    Law(
        name="E = mc²",
        formula="E = m × c²",
        func=lambda m: m * C ** 2,
        test_cases=[
            {"input": (1,), "expected": C ** 2},
            {"input": (0.001,), "expected": 0.001 * C ** 2},
        ],
    ),

    # 5. طاقة الفوتون
    Law(
        name="E = h·f",
        formula="E = h × f",
        func=lambda f: H * f,
        test_cases=[
            {"input": (1,), "expected": H},
            {"input": (5e14,), "expected": H * 5e14},
        ],
    ),

    # 6. الجاذبية
    Law(
        name="قانون الجذب العام",
        formula="F = G·m₁·m₂/r²",
        func=lambda m1, m2, r: G * m1 * m2 / r ** 2,
        test_cases=[
            {"input": (1, 1, 1), "expected": G},
            {"input": (10, 10, 2), "expected": G * 100 / 4},
        ],
    ),

    # 7. الغاز المثالي
    Law(
        name="قانون الغاز المثالي",
        formula="P = nRT/V",
        func=lambda n, V, T: n * R_GAS * T / V,
        test_cases=[
            {"input": (1, 1, 273.15), "expected": R_GAS * 273.15},
            {"input": (2, 2, 300), "expected": R_GAS * 300},
        ],
    ),

    # 8. كفاءة كارنو
    Law(
        name="كفاءة كارنو",
        formula="η = 1 - Tc/Th",
        func=lambda Th, Tc: 1 - Tc / Th,
        test_cases=[
            {"input": (500, 300), "expected": 0.4},
            {"input": (300, 300), "expected": 0.0},
            {"input": (1000, 200), "expected": 0.8},
        ],
    ),

    # 9. السرعة الحرجة (الهروب)
    Law(
        name="سرعة الهروب",
        formula="v = √(2GM/r)",
        func=lambda M, r: math.sqrt(2 * G * M / r),
        test_cases=[
            # الأرض: M=5.97e24, r=6.371e6 → v ≈ 11186 m/s
            {"input": (5.97e24, 6.371e6), "expected": 11184.1},
        ],
    ),

    # 10. تحويل كلفن إلى مئوية
    Law(
        name="تحويل كلفن → مئوية",
        formula="°C = K - 273.15",
        func=lambda K: K - 273.15,
        test_cases=[
            {"input": (273.15,), "expected": 0.0},
            {"input": (373.15,), "expected": 100.0},
            {"input": (0,), "expected": -273.15},
        ],
    ),
]
