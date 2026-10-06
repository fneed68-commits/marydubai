#!/usr/bin/env python3
"""
MaryDubai Sales Receipt Generator
يولّد تقرير احترافي لكل عملية اشتراك
"""
import json
import os
from datetime import datetime
from pathlib import Path


class ReceiptGenerator:
    def __init__(self, log_file="./sales_log.json"):
        self.log_file = log_file
        self.log = self._load_log()
        self.company = {
            "name_ar": "ماري دبي",
            "name_en": "MaryDubai",
            "email": "fneed68@gmail.com",
            "discord": "https://discord.gg/HCb4ufeQDq",
            "website": "https://payhip.com/marydubai",
        }
        self.product = {
            "name_ar": "نظام ماري دبي متعدد الوكلاء",
            "name_en": "MaryDubai Multi-Agent System",
            "version": "v1.0",
            "description_ar": "نظام 7 وكلاء ذكاء اصطناعي مع تحكم بشري صارم",
            "description_en": "7 AI Agents with Strict Human-in-the-Loop",
            "features_ar": [
                "7 وكلاء متخصصين",
                "74 اختبار ناجح (100%)",
                "كود المصدر الكامل",
                "رخصة تجارية",
                "دعم 30 يوم",
                "تحديثات مجانية 6 أشهر",
            ],
        }

    def _load_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"sales": [], "total_revenue": 0}

    def _save_log(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)

    def generate_receipt(
        self,
        customer_name,
        customer_email,
        amount,
        currency="USD",
        payment_method="YousrPay",
        transaction_id=None,
        tier="Starter",
    ):
        """يولّد تقرير اشتراك جديد"""
        # رقم الطلب
        order_number = f"MD-{datetime.now().strftime('%Y%m%d')}-{len(self.log['sales']) + 1:04d}"
        
        # وقت الإصدار
        issue_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        receipt = {
            "order_number": order_number,
            "issue_date": issue_date,
            "customer": {
                "name": customer_name,
                "email": customer_email,
            },
            "product": self.product,
            "payment": {
                "amount": amount,
                "currency": currency,
                "method": payment_method,
                "transaction_id": transaction_id or f"TXN-{order_number}",
                "tier": tier,
                "status": "مدفوع ✅ / Paid ✅",
            },
            "company": self.company,
        }

        # سجل البيع
        self.log["sales"].append(receipt)
        self.log["total_revenue"] += amount
        self._save_log()

        return receipt

    def format_arabic(self, receipt):
        """صيغة عربية"""
        r = receipt
        lines = []
        lines.append("═" * 60)
        lines.append("🎯 إيصال اشتراك رسمي")
        lines.append("═" * 60)
        lines.append("")
        lines.append(f"📋 رقم الطلب:  {r['order_number']}")
        lines.append(f"📅 تاريخ الإصدار: {r['issue_date']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("👤 معلومات العميل")
        lines.append("─" * 60)
        lines.append(f"   الاسم:  {r['customer']['name']}")
        lines.append(f"   البريد: {r['customer']['email']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📦 المنتج")
        lines.append("─" * 60)
        lines.append(f"   الاسم:  {r['product']['name_ar']}")
        lines.append(f"   النسخة: {r['product']['version']}")
        lines.append(f"   الوصف:  {r['product']['description_ar']}")
        lines.append("")
        lines.append("   المميزات:")
        for feat in r['product']['features_ar']:
            lines.append(f"     ✓ {feat}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("💳 تفاصيل الدفع")
        lines.append("─" * 60)
        lines.append(f"   الباقة:  {r['payment']['tier']}")
        lines.append(f"   المبلغ:  {r['payment']['amount']} {r['payment']['currency']}")
        lines.append(f"   الطريقة: {r['payment']['method']}")
        lines.append(f"   رقم المعاملة: {r['payment']['transaction_id']}")
        lines.append(f"   الحالة:  {r['payment']['status']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📥 خطوات التحميل")
        lines.append("─" * 60)
        lines.append("   1. افتح الرابط التالي:")
        lines.append("      https://payhip.com/b/eP6gb")
        lines.append("")
        lines.append("   2. أدخل بريدك الإلكتروني:")
        lines.append(f"      {r['customer']['email']}")
        lines.append("")
        lines.append("   3. حمّل الملف:")
        lines.append("      marydubai_v1.0_RELEASE.tar.gz")
        lines.append("")
        lines.append("   4. فك الضغط:")
        lines.append("      tar -xzf marydubai_v1.0_RELEASE.tar.gz")
        lines.append("")
        lines.append("   5. شغّل العرض التجريبي:")
        lines.append("      bash demo.sh")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📞 الدعم الفني (30 يوم)")
        lines.append("─" * 60)
        lines.append(f"   📧 البريد: {r['company']['email']}")
        lines.append(f"   💬 Discord: {r['company']['discord']}")
        lines.append(f"   🌐 الموقع: {r['company']['website']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("✅ شكراً لثقتك بنا!")
        lines.append("─" * 60)
        lines.append("")
        lines.append("هذا الإيصال صادر إلكترونياً ولا يحتاج ختماً.")
        lines.append(f"© 2026 {r['company']['name_ar']} - جميع الحقوق محفوظة")
        lines.append("═" * 60)
        return "\n".join(lines)

    def format_english(self, receipt):
        """English format"""
        r = receipt
        lines = []
        lines.append("═" * 60)
        lines.append("🎯 Official Subscription Receipt")
        lines.append("═" * 60)
        lines.append("")
        lines.append(f"📋 Order Number: {r['order_number']}")
        lines.append(f"📅 Issue Date:   {r['issue_date']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("👤 Customer Information")
        lines.append("─" * 60)
        lines.append(f"   Name:  {r['customer']['name']}")
        lines.append(f"   Email: {r['customer']['email']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📦 Product")
        lines.append("─" * 60)
        lines.append(f"   Name:    {r['product']['name_en']}")
        lines.append(f"   Version: {r['product']['version']}")
        lines.append(f"   Desc:    {r['product']['description_en']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("💳 Payment Details")
        lines.append("─" * 60)
        lines.append(f"   Tier:     {r['payment']['tier']}")
        lines.append(f"   Amount:   {r['payment']['amount']} {r['payment']['currency']}")
        lines.append(f"   Method:   {r['payment']['method']}")
        lines.append(f"   TXN ID:   {r['payment']['transaction_id']}")
        lines.append(f"   Status:   {r['payment']['status']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📥 Download Instructions")
        lines.append("─" * 60)
        lines.append("   1. Open: https://payhip.com/b/eP6gb")
        lines.append(f"   2. Enter your email: {r['customer']['email']}")
        lines.append("   3. Download: marydubai_v1.0_RELEASE.tar.gz")
        lines.append("   4. Extract: tar -xzf marydubai_v1.0_RELEASE.tar.gz")
        lines.append("   5. Run demo: bash demo.sh")
        lines.append("")
        lines.append("─" * 60)
        lines.append("📞 Support (30 days)")
        lines.append("─" * 60)
        lines.append(f"   📧 Email:   {r['company']['email']}")
        lines.append(f"   💬 Discord: {r['company']['discord']}")
        lines.append(f"   🌐 Website: {r['company']['website']}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("✅ Thank you for your trust!")
        lines.append("─" * 60)
        lines.append(f"© 2026 {r['company']['name_en']} - All rights reserved")
        lines.append("═" * 60)
        return "\n".join(lines)

    def save_to_file(self, receipt, output_dir="./receipts"):
        """يحفظ التقرير كملف"""
        Path(output_dir).mkdir(exist_ok=True)
        order_num = receipt['order_number']

        # العربية
        ar_file = f"{output_dir}/{order_num}_AR.txt"
        with open(ar_file, 'w', encoding='utf-8') as f:
            f.write(self.format_arabic(receipt))
        print(f"✅ حفظ التقرير العربي: {ar_file}")

        # English
        en_file = f"{output_dir}/{order_num}_EN.txt"
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(self.format_english(receipt))
        print(f"✅ Saved English receipt: {en_file}")

        return ar_file, en_file

    def stats(self):
        """إحصائيات المبيعات"""
        total = len(self.log['sales'])
        revenue = self.log['total_revenue']
        print("═" * 60)
        print("📊 إحصائيات المبيعات")
        print("═" * 60)
        print(f"   إجمالي الاشتراكات: {total}")
        print(f"   إجمالي الإيرادات:  {revenue} USD")
        if total > 0:
            print(f"   متوسط البيع:        {revenue/total:.2f} USD")
        print("═" * 60)


if __name__ == "__main__":
    print("═" * 60)
    print("🎬 MaryDubai Receipt Generator - Demo")
    print("═" * 60)
    print()

    gen = ReceiptGenerator()

    # نموذج عميل تجريبي
    receipt = gen.generate_receipt(
        customer_name="أحمد محمد",
        customer_email="ahmed@example.com",
        amount=49,
        currency="USD",
        payment_method="YousrPay",
        transaction_id="sb_txn_demo_123",
        tier="Starter",
    )

    # حفظ
    gen.save_to_file(receipt)

    # عرض
    print()
    print(gen.format_arabic(receipt))
    print()
    gen.stats()
