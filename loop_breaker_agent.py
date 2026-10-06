import hashlib
import time

class LoopBreakerAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-AntiLoopGuard"
        self.analysis_registry = {}
        # تحديد عتبات استهلاك الذاكرة وفق قوانين المنظومة المثبتة
        self.ram_warning_threshold = 70.0
        self.ram_safe_threshold = 67.0

    def should_break_loop(self, step_action, step_result):
        """
        القانون الأول: مطابقة بصمة (الخطوة + النتيجة) لكسر التكرار الصامت فوراً
        """
        # 1. دمج الخطوة والنتيجة في معرّف واحد وتوليد بصمة فريدة
        combined_identity = f"{step_action.strip()} -> {step_result.strip()}"
        signature = hashlib.md5(combined_identity.encode('utf-8')).hexdigest()
        
        # 2. تسجيل التكرار في السجل المحلي للوكيل
        if signature in self.analysis_registry:
            self.analysis_registry[signature] += 1
        else:
            self.analysis_registry[signature] = 1
            
        # 3. اتخاذ خطوة الكسر القسري إذا تكررت النتيجة أكثر من مرة
        if self.analysis_registry[signature] > 1:
            print(f"\n🚨 [{self.agent_name}] تنبيه! تم رصد تكرار نفس خطوات الفحص ونفس النتائج.")
            print("⚡ [قانون كسر الحلقة] جاري تفعيل الإجراء الخارجي القسري للخروج من الحلقة المفرغة...")
            return True # يجب كسر الحلقة فوراً
            
        return False # المسار سليم

    def monitor_resources(self, current_ram_usage):
        """
        القانون الثاني: فحص استقرار الذاكرة العشوائية وتحديد لون المؤشر
        """
        print(f"📊 [{self.agent_name}] فحص الموارد الحالية للـ RAM: {current_ram_usage}%")
        
        if current_ram_usage >= self.ram_warning_threshold:
            print("🟡 [مؤشر أصفر - خطأ صامت] استهلاك الذاكرة تجاوز 70%! اشتباه في وجود تسريب أو حلقة معلقة.")
            return "YELLOW"
        elif current_ram_usage <= self.ram_safe_threshold:
            print("🟢 [مؤشر أخضر - مستقر] استهلاك الذاكرة آمن وتحت عتبة 67%.")
            return "GREEN"
        else:
            print("⚪ [وضع حيادي] الذاكرة في النطاق الانتقالي.")
            return "NEUTRAL"

    def await_director_command(self, status_message):
        """
        قانون التحكم الصارم: نفّذ الإجراء وتوقف كلياً بانتظار أمر الموجه التالي
        """
        print("\n============================================================")
        print(f"📢 [{self.agent_name}] الوكيل متوقف حالياً لتلقي التعليمات.")
        print(f"📝 حالة النظام الحالية: {status_message}")
        print("============================================================")
        
        command = input("👤 [الموجه كابتن] هل توافق على تجاوز هذه النقطة والانتقال للملف التالي؟ (yes/no): ")
        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم كسر التكرار بنجاح والانتقال للمسار التالي...")
            return True
        else:
            print("🛑 [أمر تجميد] تم الإبقاء على الوضع الحالي دون تغيير بناءً على رغبتك.")
            return False

# تشغيل الفحص التجريبي الحي للوكيل الثاني
if __name__ == "__main__":
    breaker_agent = LoopBreakerAgent()
    
    # محاكاة خطوة متكررة خرجت بنفس النتيجة مرتين (محاكاة حلقة لانهائية)
    action_sample = "تحليل الاستعلام البرمجي لـ API هكروان"
    result_sample = "HTTPConnectionPool(host='10.255.255.254'): Connection refused"
    
    # محاكاة فحص الموارد (تجاوز الـ 70% كمثال لاختبار الإنذار الأصفر)
    breaker_agent.monitor_resources(72.5)
    
    # فحص الخطوة الأولى (تسجيل عادي)
    breaker_agent.should_break_loop(action_sample, result_sample)
    
    # فحص الخطوة الثانية (تكرار نفس المدخلات والنتائج)
    if breaker_agent.should_break_loop(action_sample, result_sample):
        breaker_agent.await_director_command("تم رصد حلقة لانهائية وتجميد المعالج بنجاح.")
