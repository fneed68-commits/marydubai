import json
import os

class LegalConsultantAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-LegalGuard"
        # قاعدة البيانات القانونية المصغرة للتحقق الأولي (سيتم ربطها بملفات الـ RAG لاحقاً)
        self.compliance_frameworks = {
            "HackerOne_Policy": "In-Scope verification required, No destructive payloads, No automated brute-force.",
            "NIST_800_53": "Access Control, Risk Assessment, and Audit Logging compliance standards.",
            "IP_Protection": "Original work verification, Non-derivative software enforcement."
        }

    def audit_action_compliance(self, proposed_action, context_data):
        """
        القانون الأول: فحص الامتثال القانوني الشامل وتحديد نقاط النجاح والفشل
        """
        print(f"\n⚖️ [{self.agent_name}] جاري التدقيق القانوني والامتثالي للإجراء المقترح...")
        
        # 1. التحقق من الامتثال لسياسات المنصات والنطاق
        if context_data.get("is_automated_spam", False):
            print("❌ [فشل الامتثال القانوني] الإجراء ينتهك سياسة مكافحة الفحص العشوائي المضلل!")
            return False
            
        # 2. التحقق من حماية الحقوق الفكرية والأصالة
        if not context_data.get("is_original_work", True):
            print("❌ [فشل الملكية الفكرية] تم رصد اشتباه في اشتقاق أو تعد تعدي على حقوق ملكية!")
            return False

        print("✅ [نجاح التدقيق الأولي] الإجراء البرمجي متوافق مع لوائح الامتثال ومحمي قانونياً.")
        return True

    def await_human_command(self, action_details):
        """
        قانون التحكم الصارم: نفّذ الأمر وتوقف كلياً بانتظار الموجه البشري
        """
        print("\n============================================================")
        print(f"📢 [تنبيه مستشار القوانين] تم الانتهاء من صياغة تقرير الامتثال.")
        print(f"📄 الإجراء الخاضع للرقابة: {action_details}")
        print("============================================================")
        
        # التوقف القسري بانتظار أمرك التالي خطوة بخطوة
        command = input("👤 [الموجه كابتن] هل توافق على تمرير هذا الإجراء قانونياً؟ (اكتب 'yes' للموافقة / أي زر آخر للتجميد): ")
        
        if command.strip().lower() == 'yes':
            print("🚀 [أمر تمرير] تم اعتماد القرار قانونياً من الموجه البشري. جاري التنفيذ...")
            return True
        else:
            print("🛑 [أمر التجميد القسري] تم إيقاف وتجميد العملية بناءً على أمر الموجه الخارجي.")
            return False

# تشغيل الفحص التجريبي الأولي للوكيل الأول
if __name__ == "__main__":
    agent = LegalConsultantAgent()
    
    # محاكاة إجراء سيبراني أو استثماري يراد اختباره
    action_desc = "تقديم تقرير ثغرة مكتشفة في تحدي CTF 232 إلى HackerOne"
    mock_context = {"is_automated_spam": False, "is_original_work": True}
    
    # تنفيذ الفحص
    if agent.audit_action_compliance(action_desc, mock_context):
        agent.await_human_command(action_desc)
