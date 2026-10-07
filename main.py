#!/usr/bin/env python3
# main.py
"""
MaryDubai Multi-Agent System - نقطة الدخول الموحّدة
=====================================================
الاستخدام:
  python3 main.py --list
  python3 main.py --agent rag --query "ما هي الثغرات؟"
  python3 main.py --agent rag --index ./docs
  python3 main.py --agent legal --action "..."
  python3 main.py --agent loop --action "..." --result "..."
  python3 main.py --agent temporal --time 1.2
  python3 main.py --agent financial --target "..." --revenue 1000 --cost 500 --risk 0.3
  python3 main.py --agent math --calc semiconductor --voltage 0.7 --temp 300
  python3 main.py --agent wallet --address "0x..." --network ethereum
"""
import argparse
import sys
import os
from pathlib import Path

# === Registry of all agents ===
AGENTS = {
    "rag": {
        "module": "rag_time_manager_agent",
        "class": "RAGTimeManagerAgent",
        "description": "وكيل RAG - بحث ذكي في قاعدة معرفة",
        "use_local": True,  # default to local embedder
    },
    "legal": {
        "module": "legal_consultant_agent",
        "class": "LegalConsultantAgent",
        "description": "المستشار القانوني - تدقيق الامتثال",
    },
    "loop": {
        "module": "loop_breaker_agent",
        "class": "LoopBreakerAgent",
        "description": "كسر الحلقات اللانهائية",
    },
    "temporal": {
        "module": "temporal_edge_agent",
        "class": "TemporalEdgeAgent",
        "description": "الحواف الزمنية - فحص الحدود الزمنية",
    },
    "financial": {
        "module": "financial_investment_agent",
        "class": "FinancialInvestmentAgent",
        "description": "الاستثمار المالي - تحليل العوائد",
    },
    "math": {
        "module": "math_physics_agent",
        "class": "MathPhysicsAgent",
        "description": "الرياضيات والفيزياء",
    },
    "wallet": {
        "module": "wallet_security_agent",
        "class": "WalletSecurityAgent",
        "description": "أمن المحافظ الإلكترونية",
    },
}


def print_banner():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║  🎯 MaryDubai Multi-Agent System v1.0" + " " * 20 + "║")
    print("║  نظام وكلاء متعدد مع تحكم بشري صارم (HITL)" + " " * 12 + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def cmd_list():
    """عرض كل الوكلاء"""
    print_banner()
    print("📋 الوكلاء المتاحون:\n")
    for name, info in AGENTS.items():
        print(f"  [{name:>10}]  {info['description']}")
    print()
    print("💡 أمثلة:")
    print("  python3 main.py --agent rag --query 'ما هي الثغرات؟'")
    print("  python3 main.py --agent legal --action 'تقرير CTF'")
    print("  python3 main.py --agent temporal --time 1.2")
    print()


def load_agent(agent_name):
    """تحميل وكيل بالاسم"""
    if agent_name not in AGENTS:
        print(f"❌ وكيل غير معروف: {agent_name}")
        print(f"   المتاح: {', '.join(AGENTS.keys())}")
        sys.exit(1)

    info = AGENTS[agent_name]
    try:
        module = __import__(info["module"])
        agent_class = getattr(module, info["class"])
        return agent_class
    except ImportError as e:
        print(f"❌ فشل تحميل الوكيل '{agent_name}': {e}")
        sys.exit(1)
    except AttributeError as e:
        print(f"❌ الكلاس '{info['class']}' غير موجود في '{info['module']}': {e}")
        sys.exit(1)


# === Command handlers per agent ===

def run_rag(args):
    Agent = load_agent("rag")
    agent = Agent(
        db_path=args.db,
        use_local_embedder=args.use_local
    )

    if args.index:
        # بناء Index
        source = Path(args.index)
        if not source.exists():
            print(f"❌ المسار غير موجود: {source}")
            return 1
        content = source.read_text(encoding="utf-8", errors="ignore") if source.is_file() else ""
        if content:
            agent.index_document(content, metadata={"source": str(source)})
        else:
            print("⚠️ استخدم index_builder.py لفهرسة المجلدات")
        return 0

    if args.query:
        summary = agent.analyze_with_context(args.query)
        if summary.get("status") == "OK":
            approved = agent.await_captain_command(summary)
            if approved:
                agent.log_decision("approved", [c["metadata"].get("chunk_index", 0) for c in summary["contexts"]])
                print("\n📊 ملخص الجلسة:")
                print(f"   {agent.get_session_summary()}")
        else:
            print("⚠️ لا توجد نتائج للاستعلام.")
        return 0

    print("⚠️ استخدم --query أو --index")
    return 1


def run_legal(args):
    Agent = load_agent("legal")
    agent = Agent()
    action = args.action or "إجراء افتراضي"
    context = {
        "is_automated_spam": False,
        "is_original_work": True,
    }
    if agent.audit_action_compliance(action, context):
        agent.await_human_command(action)
    return 0


def run_loop(args):
    Agent = load_agent("loop")
    agent = Agent()
    action = args.action or "خطوة افتراضية"
    result = args.result or "نتيجة افتراضية"
    # نستدعي الوكيل مرتين لمحاكاة تكرار (الغرض من الوكيل كشف التكرار)
    print(f"🔄 [محاكاة] استدعاء 1: {action} -> {result}")
    if agent.should_break_loop(action, result):
        agent.await_director_command("تم كسر الحلقة")
        return 0
    print(f"🔄 [محاكاة] استدعاء 2: {action} -> {result} (تكرار)")
    if agent.should_break_loop(action, result):
        agent.await_director_command("تم رصد حلقة لا نهائية")
    return 0


def run_temporal(args):
    Agent = load_agent("temporal")
    agent = Agent()
    time_value = float(args.time) if args.time else 1.2
    if not agent.test_lower_time_limit(time_value):
        agent.await_captain_decision("فحص الحافة الزمنية")
    return 0


def run_financial(args):
    Agent = load_agent("financial")
    agent = Agent()
    target = args.target or "هدف افتراضي"
    revenue = float(args.revenue) if args.revenue else 1000.0
    cost = float(args.cost) if args.cost else 500.0
    risk = float(args.risk) if args.risk else 0.3
    result = agent.analyze_profit_target(target, revenue, cost, risk)
    if hasattr(agent, 'await_captain_command'):
        agent.await_captain_command(str(result))
    return 0


def run_math(args):
    Agent = load_agent("math")
    agent = Agent()
    calc = args.calc or "semiconductor"
    if calc == "semiconductor":
        v = float(args.voltage) if args.voltage else 0.7
        t = float(args.temp) if args.temp else 300.0
        result = agent.calculate_semiconductor_current(v, t)
        print(f"✅ النتيجة: {result}")
    elif calc == "audience":
        t = float(args.time) if args.time else 10.0
        i = int(args.interaction) if args.interaction else 5
        result = agent.calculate_audience_points(t, i)
        print(f"✅ النتيجة: {result}")
    else:
        print(f"❌ نوع الحساب غير معروف: {calc}")
    return 0


def run_wallet(args):
    Agent = load_agent("wallet")
    agent = Agent()
    if args.address:
        valid = agent.verify_wallet_address(args.address, args.network or "ethereum")
        print(f"✅ النتيجة: {'صالح' if valid else 'غير صالح'}")
        agent.await_mojeh_approval(f"التحقق من {args.address}")
    elif args.command:
        agent.verify_command_intent(args.command)
    else:
        print("⚠️ استخدم --address أو --command")
    return 1


# === Dispatcher ===
HANDLERS = {
    "rag": run_rag,
    "legal": run_legal,
    "loop": run_loop,
    "temporal": run_temporal,
    "financial": run_financial,
    "math": run_math,
    "wallet": run_wallet,
}


def main():
    parser = argparse.ArgumentParser(
        description="MaryDubai Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="استخدم --list لعرض الوكلاء"
    )
    parser.add_argument("--list", action="store_true", help="عرض كل الوكلاء")
    parser.add_argument("--agent", "-a", help="اسم الوكيل")
    parser.add_argument("--query", "-q", help="[rag] استعلام البحث")
    parser.add_argument("--index", help="[rag] مسار ملف للفهرسة")
    parser.add_argument("--db", default="./rag_index.db", help="[rag] مسار قاعدة البيانات")
    parser.add_argument("--use-local", action="store_true", help="[rag] استخدام embedder محلي بدل Gemini")
    parser.add_argument("--action", help="[legal/loop] الإجراء")
    parser.add_argument("--result", help="[loop] النتيجة")
    parser.add_argument("--time", help="[temporal/math] الزمن")
    parser.add_argument("--target", help="[financial] الهدف")
    parser.add_argument("--revenue", help="[financial] الإيراد المتوقع")
    parser.add_argument("--cost", help="[financial] التكلفة")
    parser.add_argument("--risk", help="[financial] عامل المخاطرة")
    parser.add_argument("--calc", help="[math] نوع الحساب")
    parser.add_argument("--voltage", help="[math] الجهد")
    parser.add_argument("--temp", help="[math] الحرارة")
    parser.add_argument("--interaction", help="[math] عدد التفاعلات")
    parser.add_argument("--address", help="[wallet] عنوان المحفظة")
    parser.add_argument("--network", help="[wallet] الشبكة")
    parser.add_argument("--command", help="[wallet] الأمر")

    args = parser.parse_args()

    if args.list or not args.agent:
        cmd_list()
        return 0

    handler = HANDLERS.get(args.agent)
    if not handler:
        print(f"❌ وكيل غير مدعوم: {args.agent}")
        return 1

    return handler(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n🛑 تم الإيقاف بواسطة المستخدم.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        sys.exit(1)
