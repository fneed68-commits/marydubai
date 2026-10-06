#!/usr/bin/env python3
"""
New Sale - Interactive Receipt Generator
أداة تفاعلية لتوليد إيصال بسرعة
"""
from receipt_generator import ReceiptGenerator


def ask(prompt, default=""):
    """طلب إدخال مع قيمة افتراضية"""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


def main():
    print()
    print("═" * 60)
    print("🛒  تسجيل عملية بيع جديدة")
    print("═" * 60)
    print()
    print("💡 اضغط Enter لقبول القيمة الافتراضية")
    print()

    # بيانات العميل
    print("─" * 60)
    print("👤 بيانات العميل")
    print("─" * 60)
    name = ask("   الاسم")
    if not name:
        print("❌ الاسم مطلوب")
        return
    email = ask("   البريد الإلكتروني")
    if not email:
        print("❌ البريد مطلوب")
        return

    # الدفع
    print()
    print("─" * 60)
    print("💳 تفاصيل الدفع")
    print("─" * 60)
    amount = float(ask("   المبلغ", "49"))
    currency = ask("   العملة", "USD")
    method = ask("   طريقة الدفع", "YousrPay")
    txn = ask("   رقم المعاملة (اختياري)", "")
    tier = ask("   الباقة", "Starter")

    # توليد الإيصال
    print()
    print("─" * 60)
    print("⏳ جاري توليد الإيصال...")
    print("─" * 60)

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
    print(f"✅ تم إنشاء الإيصال: {receipt['order_number']}")
    print("═" * 60)
    print()
    print(f"📁 الملفات:")
    print(f"   AR: {ar_file}")
    print(f"   EN: {en_file}")
    print()
    print("─" * 60)
    print("📧 محتوى البريد للعميل:")
    print("─" * 60)
    print()
    print(f"الموضوع: تأكيد اشتراكك - {receipt['order_number']}")
    print()
    print(f"عزيزي {name}،")
    print()
    print(f"شكراً لاشتراكك في نظام ماري دبي متعدد الوكلاء!")
    print()
    print(f"📋 رقم الطلب: {receipt['order_number']}")
    print(f"💰 المبلغ: {amount} {currency}")
    print(f"💳 طريقة الدفع: {method}")
    print()
    print("📥 خطوات التحميل:")
    print(f"   1. افتح: https://payhip.com/b/eP6gb")
    print(f"   2. أدخل بريدك: {email}")
    print(f"   3. حمّل: marydubai_v1.0_RELEASE.tar.gz")
    print(f"   4. فك الضغط: tar -xzf marydubai_v1.0_RELEASE.tar.gz")
    print(f"   5. شغّل: bash demo.sh")
    print()
    print("📞 الدعم:")
    print("   📧 fneed68@gmail.com")
    print("   💬 discord.gg/HCb4ufeQDq")
    print()
    print("مع تحيات فريق ماري دبي")
    print()
    print("─" * 60)
    print()
    print("💡 نسخ الإيصال الكامل:")
    print(f"   cat {ar_file}")
    print()
    print("═" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 تم الإلغاء")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
