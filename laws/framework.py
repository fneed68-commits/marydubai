#!/usr/bin/env python3
"""
إطار اختبار القوانين
كل قانون = دالة + حالات اختبار
"""

class Law:
    def __init__(self, name, formula, func, test_cases, description=""):
        self.name = name
        self.formula = formula
        self.func = func
        self.test_cases = test_cases
        self.description = description

    def test(self, tolerance=1e-6):
        """يختبر القانون ويعيد النتائج (مع تسامح نسبي للأرقام الكبيرة)"""
        results = []
        for i, case in enumerate(self.test_cases, 1):
            inputs = case["input"]
            expected = case["expected"]
            try:
                actual = self.func(*inputs)
                # مقارنة مع التسامح
                if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
                    # تسامح نسبي للأرقام الكبيرة (>1)
                    if abs(expected) > 1:
                        passed = abs(actual - expected) / abs(expected) < 1e-4
                    else:
                        passed = abs(actual - expected) < tolerance
                else:
                    passed = actual == expected
                results.append({
                    "case": i,
                    "inputs": inputs,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed,
                })
            except Exception as e:
                results.append({
                    "case": i,
                    "inputs": inputs,
                    "expected": expected,
                    "actual": f"ERROR: {e}",
                    "passed": False,
                })
        return results

    def passed(self):
        """هل اجتاز كل الاختبارات؟"""
        return all(r["passed"] for r in self.test())


class LawRegistry:
    def __init__(self):
        self.laws = []

    def add(self, law):
        self.laws.append(law)

    def run_all(self, verbose=True):
        """يشغل كل القوانين"""
        total = len(self.laws)
        passed = 0
        failed = 0
        failed_laws = []

        for law in self.laws:
            results = law.test()
            all_passed = all(r["passed"] for r in results)

            if all_passed:
                passed += 1
                if verbose:
                    print(f"✅ {law.name}")
                    print(f"   {law.formula}")
            else:
                failed += 1
                failed_laws.append(law)
                if verbose:
                    print(f"❌ {law.name}")
                    print(f"   {law.formula}")
                    for r in results:
                        if not r["passed"]:
                            print(f"   ├─ حالة {r['case']}: {r['inputs']}")
                            print(f"   │   متوقع: {r['expected']}")
                            print(f"   │   فعلي:  {r['actual']}")
                    print()

        print("=" * 60)
        print(f"📊 النتيجة: {passed}/{total} نجح، {failed} فشل")
        print("=" * 60)

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "failed_laws": failed_laws,
        }
