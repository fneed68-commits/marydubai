import math

class MathPhysicsAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-MathPhysGuard"
        # ثوابت فيزيائية إلكترونية أساسية
        self.ELECTRON_CHARGE = 1.602e-19  # كولوم
        self.BOLTZMANN_CONSTANT = 1.380e-23  # جول/كلفن

    def calculate_semiconductor_current(self, voltage, temperature_k, saturation_current=1e-12):
        """
        القانون الأول: نمذجة تيار أشباه الموصلات (معادلة ديود شوكلي) بدقة فيزيائية
        """
        print(f"\n⚡ [{self.agent_name}] جاري تحليل الفيزياء الإلكترونية للقطعة البرمجية...")
        
        # حساب الجهد الحراري (Thermal Voltage = k*T/q)
        thermal_voltage = (self.BOLTZMANN_CONSTANT * temperature_k) / self.ELECTRON_CHARGE
        
        try:
            # تطبيق المعادلة الفيزيائية الحاكمة للتيار
            exponent = voltage / thermal_voltage
            # حماية النظام من الحسابات اللانهائية أو التضخم الإسّي القاتل للذاكرة
            if exponent > 50:
                print("⚠️ [تنبيه فيزيائي] الجهد المرتفع قد يؤدي لتضخم إسّي خطر! تم كسر الحساب لحماية الموارد.")
                return None
                
            diode_current = saturation_current * (math.exp(exponent) - 1)
            print(f"✅ [نجاح النمذجة] الحسابات الفيزيائية دقيقة. التيار المستنتج: {diode_current:.4e} أمبير.")
            return diode_current
        except Exception as e:
            print(f"❌ [خطأ رياضي] فشل في معالجة المعادلة الفيزيائية: {str(e)}")
            return None

    def calculate_audience_points(self, time_spent_minutes, interaction_count):
        """
        القانون الثاني: احتساب نقاط تحفيز الجمهور بناءً على المنهجية الرياضية الصارمة
        """
        print(f"📊 [{self.agent_name}] جاري احتساب معادلة الأرباح ونقاط الجمهور...")
        
        # قانون رياضي تصاعدي لحساب النقاط: (الوقت * معامل التفاعل) مع سقف لوغاريتمي لمنع التلاعب
        if time_spent_minutes <= 0:
            return 0.0
            
        base_points = time_spent_minutes * (interaction_count + 1)
        final_score = base_points * math.log10(time_spent_minutes + 9)
        
        print(f"✅ [نجاح الحساب] النقاط المستحقة بدقة: {final_score:.2f} نقطة.")
        return final_score

    def await_mojeh_command(self, calculation_summary):
        """
        قانون التحكم الصارم: نفّذ الأمر وتوقف كلياً بانتظار الموجه البشري
        ```
        """
        print("\n============================================================")
        print(f"📢 [{self.agent_name}] تم استكمال المعالجات الرياضية والفيزيائية.")
        print(f"📝 ملخص المخرجات الحالية: {calculation_summary}")
        print("============================================================")
        
        command = input("👤 [الموجه كابتن] هل توافق على اعتماد هذه النتائج الرياضية وتمريرها؟ (yes/no): ")
        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم قفل الحسابات واعتماد النتائج بنجاح.")
            return True
        else:
            print("🛑 [أمر تجميد قسري] تم إلغاء الاعتماد وتجميد مخرجات الوكيل الثالث.")
            return False

if __name__ == "__main__":
    math_phys = MathPhysicsAgent()
    
    # 1. اختبار نمذجة الفيزياء الإلكترونية (جهد 0.5 فولت، حرارة 300 كلفن الغرفة الافتراضية)
    current_res = math_phys.calculate_semiconductor_current(voltage=0.5, temperature_k=300)
    
    # 2. اختبار معادلة الرياضيات لنظام النقاط (بقاء 45 دقيقة مع 5 تفاعلات)
    points_res = math_phys.calculate_audience_points(time_spent_minutes=45, interaction_count=5)
    
    # 3. بوابة التوقف المطلق للتحكم البشري
    if current_res and points_res:
        summary = f"تيار شبه الموصل = {current_res:.4e} A | نقاط الجمهور المحسوبة = {points_res:.2f}"
        math_phys.await_mojeh_command(summary)
