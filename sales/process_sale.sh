#!/data/data/com.termux/files/usr/bin/bash
# سكربت موحد: يربط الإيصال + Discord + السجل

cd ~/termux_secops_project/sales

echo "════════════════════════════════════════════"
echo "🎯 MaryDubai - معالجة بيع جديد"
echo "════════════════════════════════════════════"
echo ""

# 1. اطلب بيانات العميل
echo "👤 بيانات العميل:"
read -p "   الاسم: " CUSTOMER
read -p "   البريد: " EMAIL

echo ""
echo "💳 بيانات الدفع:"
read -p "   المبلغ [49]: " AMOUNT
AMOUNT=${AMOUNT:-49}

read -p "   العملة [USD]: " CURRENCY
CURRENCY=${CURRENCY:-USD}

read -p "   طريقة الدفع [YousrPay]: " METHOD
METHOD=${METHOD:-YousrPay}

read -p "   رقم المعاملة (اختياري): " TXN
read -p "   الباقة [Starter]: " TIER
TIER=${TIER:-Starter}

echo ""
echo "════════════════════════════════════════════"
echo "📋 تأكيد:"
echo "   العميل: $CUSTOMER"
echo "   المبلغ: $AMOUNT $CURRENCY"
echo "   الدفع: $METHOD"
echo "════════════════════════════════════════════"
read -p "✅ متابعة؟ (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "🛑 تم الإلغاء"
    exit 0
fi

# 2. توليد الإيصال
echo ""
echo "⏳ جولة 1: توليد الإيصال..."

python3 << PYEOF
from receipt_generator import ReceiptGenerator

gen = ReceiptGenerator()
receipt = gen.generate_receipt(
    customer_name="$CUSTOMER",
    customer_email="$EMAIL",
    amount=$AMOUNT,
    currency="$CURRENCY",
    payment_method="$METHOD",
    transaction_id="$TXN" or None,
    tier="$TIER",
)
ar_file, en_file = gen.save_to_file(receipt)

# اطبع رقم الطلب
print(f"ORDER_NUMBER={receipt['order_number']}")
PYEOF

# استخرج رقم الطلب
ORDER_NUMBER=$(ls -t receipts/*_AR.txt 2>/dev/null | head -1 | xargs basename 2>/dev/null | sed 's/_AR.txt//')

if [ -z "$ORDER_NUMBER" ]; then
    echo "❌ فشل توليد الإيصال"
    exit 1
fi

echo "✅ تم توليد الإيصال: $ORDER_NUMBER"

# 3. إرسال إشعار Discord
echo ""
echo "⏳ جولة 2: إرسال إشعار Discord..."

if [ -f ~/.marydubai/notify_sale.sh ]; then
    bash ~/.marydubai/notify_sale.sh \
        "$CUSTOMER" \
        "$AMOUNT" \
        "$CURRENCY" \
        "$ORDER_NUMBER" \
        "$METHOD"
    echo "✅ تم إرسال الإشعار"
else
    echo "⚠️ notify_sale.sh غير موجود"
fi

# 4. عرض الإيصال
echo ""
echo "════════════════════════════════════════════"
echo "📄 الإيصال الجاهز:"
echo "════════════════════════════════════════════"
echo ""
cat "receipts/${ORDER_NUMBER}_AR.txt" 2>/dev/null

echo ""
echo "════════════════════════════════════════════"
echo "✅ اكتمل بنجاح!"
echo ""
echo "📋 ملخص:"
echo "   رقم الطلب: $ORDER_NUMBER"
echo "   الإيصال: receipts/${ORDER_NUMBER}_AR.txt"
echo "   Discord: تم الإرسال إلى #sales"
echo "════════════════════════════════════════════"
