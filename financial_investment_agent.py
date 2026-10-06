import json

class FinancialInvestmentAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-FinanceGuard"
        # تحديد الحدود المالية الآمنة للمنظومة
        self.max_acceptable_risk = 0.25  # نسبة مخاطرة قصوى 25%
        self.min_acceptable_roi = 0.15   # حد أدنى للعائد 15%

    def analyze_profit_target(self, target_name, expected_revenue, initial_cost, risk_factor):
        """
        القانون الأول: تقييم جدوى أهداف الأرباح المادية والمخاطر
        """
        print(f"\n💰 [{self.agent_name}] جاري التحليل المالي والاستثماري لهدف الأرباح...")
        
        if initial_cost <= 0:
            print("❌ [خطأ مالي] التكلفة الأولية يجب أن تكون أكبر من الصفر!")
            return None
            
        # 1. احتساب العائد على الإستثمار المالي (ROI)
        net_profit = expected_revenue - initial_cost
        roi = net_profit / initial_cost
        
        print(f"📊 معدل العائد المتوقع (ROI): {roi * 100:.2f}%")
        print(f"⚠️ مستوى المخاطرة المرصود: {risk_factor * 100:.2f}%")
        
        # 2. تطبيق القوانين المالية الحاكمة للنجاح والفشل
        if roi < self.min_acceptable_roi:
            print(f"❌ [فشل استثماري] الهدف المالي مرفوض! العائد أقل من الحد الأدنى ({self.min_acceptable_roi * 100}%).")
            return "REJECTED_LOW_ROI"
            
        if risk_factor > self.max_acceptable_risk:
            print(f"❌ [فشل أمني مالي] الهدف المالي مرفوض! المخاطرة تتجاوز الحدود الآمنة ({self.max_acceptable_risk * 100}%).")
            return "REJECTED_HIGH_RISK"
            
        print("✅ [نجاح الفحص المالي] الهدف الاستثماري متوافق تماماً مع معايير الأرباح الآمنة للمنصة.")
        return "APPROVED"

    def await_captain_command(self, assessment_summary):
        """
        قانون التحكم الصارم: نفّذ الإجراء وتوقف كلياً بانتظار الموجه البشري
        """
        print("\n============================================================")
        print(f"📢 [{self.agent_name}] تم استكمال التدقيق المالي واستنتاج مؤشرات الأرباح.")
        print(f"📝 ملخص تقرير الاستثمار الحالي: {assessment_summary}")
        print("============================================================")
        
        command = input("👤 [الموجه كابتن] هل توافق على اعتماد وتمرير هذه الخطة الاستثمارية؟ (yes/no): ")
        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم قفل التقرير المالي واعتماد هدف الأرباح بنجاح.")
            return True
        else:
            print("🛑 [أمر تجميد قسري] تم إلغاء الاعتماد وتجميد مخرجات وكيل الاستثمار المالي.")
            return False

if __name__ == "__main__":
    finance_agent = FinancialInvestmentAgent()
    
    # محاكاة خطة استثمارية لهدف أرباح مادية للمنصة
    # تكلفة تشغيلية 5000$، إيرادات متوقعة 7500$ (ROI = 50%)، ونسبة مخاطرة 15%
    target_project = "توسيع بنية الـ RAG والمخدمات المحلية"
    
    status = finance_agent.analyze_profit_target(
        target_name=target_project,
        expected_revenue=7500.0,
        initial_cost=5000.0,
        risk_factor=0.15
    )
    
    # بوابة التوقف المطلق للتحكم البشري عند نجاح الفحص
    if status == "APPROVED":
        summary_report = f"المشروع: {target_project} | الحالة: متوافق وآمن للاستثمار"
        finance_agent.await_captain_command(summary_report)
