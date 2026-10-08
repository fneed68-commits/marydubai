#!/usr/bin/env python3
"""تشغيل جميع اختبارات القوانين"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework import LawRegistry

# استيراد كل مجموعات القوانين
from laws_math import laws as math_laws
from laws_math2 import laws as math2_laws
from laws_physics import laws as physics_laws
from laws_engineering import laws as eng_laws
from laws_crypto import laws as crypto_laws


def main():
    print("=" * 60)
    print("🧪 نظام اختبار القوانين الشامل")
    print("=" * 60)
    print()

    registry = LawRegistry()

    # إضافة كل القوانين
    groups = [
        ("📐 رياضيات أساسية", math_laws),
        ("📐 رياضيات متقدمة", math2_laws),
        ("⚛️ فيزياء", physics_laws),
        ("🔧 هندسة", eng_laws),
        ("₿ تشفير", crypto_laws),
    ]

    for name, laws in groups:
        print(f"{name}: {len(laws)} قانون")
        for law in laws:
            registry.add(law)

    print()
    print(f"📚 إجمالي: {len(registry.laws)} قانون")
    print()
    print("=" * 60)
    print("🔬 بدء الاختبارات")
    print("=" * 60)
    print()

    result = registry.run_all(verbose=False)

    # ملخص فقط
    print()
    if result["failed"] == 0:
        print("🎉 كل القوانين تعمل بنجاح!")
        print(f"✅ {result['passed']}/{result['total']}")
        sys.exit(0)
    else:
        print(f"⚠️  {result['failed']} قوانين فاشلة")
        print()
        for law in result["failed_laws"]:
            print(f"❌ {law.name}")
            results = law.test()
            for r in results:
                if not r["passed"]:
                    print(f"   حالة {r['case']}: {r['inputs']}")
                    print(f"   متوقع: {r['expected']}, فعلي: {r['actual']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
