#!/usr/bin/env python3
"""
New Sale v2 - مع تحقق من المدخلات
"""
import re
from receipt_generator import ReceiptGenerator


CURRENCIES = ["USD", "LYD", "EUR", "GBP", "AED", "SAR"]
METHODS = ["YousrPay", "Edfali", "MobiCash", "Moamalat", "Sadad", "PayPal"]
TIERS = ["Starter", "Professional", "Enterprise", "White-Label"]


def ask(prompt, default="", choices=None, validator=None):
    """طلب إدخال مع التحقق"""
    if default:
        prompt_full = f"{prompt} [{default}]: "
    else:
        prompt_full = f"{prompt}: "

    if choices:
        print(f"   الخيارات: {', '.join(choices)}")

    value = input(prompt_full).strip()

    if not value and default:
        value = default

    if not value:
        return None

    if validator and not validator(value):
        print(f"   ❌ قيمة غير صحيحة")
        return ask(prompt, default, choices, validator)

    if choices and value not in choices:
        print(f"   ⚠️  '{value}' ليس خياراً صحيحاً")
        print(f"   اختر من: {', '.join(choices)}")
        return ask(prompt, default, choices, validator)

    return value


def is_email(s):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', s))


def is_positive_number(s):
    try:
        return float(s) > 0
    except ValueError:
        return False


def main():
    print()
    print("═" * 60)
    print("🛒  MaryDubai - تسجيل بيع جديد")
    print("═" * 60)
    print()

    # الاسم
    name = ask("👤 اسم العميل")
    if not name:
        print("❌ الاسم مطلوب")
        return

    # البريد
    email = ask("📧 البريد الإلكتروني", validator=is_email)
    if not email:
        print("❌ البريد مطلوب")
        return
    if not is_email(email):
        print("❌ البريد غير صحيح")
        return

    # المبلغ
    amount_str = ask("💰 المبلغ", "49", validator=is_positive_number)
    try:
        amount = float(amount_str)
    except:
        print("❌ المبلغ غير صحيح")
        return

    # العملة
    currency = ask("💵 العملة", "USD", choices=CURRENCIES)

    # طريقة الدفع
    method = ask("💳 طريقة الدفع", "YousrPay", choices=METHODS)

    # رقم المعاملة
    txn = ask("🔢 رقم المعاملة (اختياري)")

    # الباقة
    tier = ask("🎯 الباقة", "Starter", choices=TIERS)

    # تأكيد
    print()
    print("─" * 60)
    print("📋 تأكيد البيانات:")
    print("─" * 60)
    print(f"   الاسم: {name}")
    print(f"   البريد: {email}")
    print(f"   المبلغ: {amount} {currency}")
    print(f"   الدفع: {method}")
    print(f"   المعاملة: {txn or 'تلقائي'}")
    print(f"   الباقة: {tier}")
    print()
    confirm = input("✅ هل البيانات صحيحة؟ (yes/no): ").strip().lower()
    if confirm != "yes":
        print("🛑 تم الإلغاء")
        return

    # التوليد
    print()
    print("⏳ جاري التوليد...")

    gen = ReceiptGenerator()
    receipt = gen.generate_receipt(
        customer_name=name,
        customer_email=email,
        amount=amount,
        currency=currency,
        payment_method=method,
        transaction_id=txn or None,
        tier=tier,
    )

    ar_file, en_file = gen.save_to_file(receipt)

    print()
    print("═" * 60)
    print(f"✅ تم بنجاح!")
    print(f"   📋 رقم الطلب: {receipt['order_number']}")
    print(f"   📁 {ar_file}")
    print("═" * 60)
    print()
    print("📄 لنسخ الإيصال:")
    print(f"   cat {ar_file}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 تم الإلغاء")
