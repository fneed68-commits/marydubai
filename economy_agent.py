#!/usr/bin/env python3
"""
MaryDubai-EconomyGuard
وكيل التحليل الاقتصادي والمالي
مع تحكم بشري صارم (HITL)
"""
import math


class EconomyAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-EconomyGuard"
    
    # ═══════════════════════════════════════════════════════
    # 1. تحليل النمو الاقتصادي
    # ═══════════════════════════════════════════════════════
    
    def calculate_gdp_growth(self, current_gdp, previous_gdp):
        """حساب معدل نمو الناتج المحلي"""
        if previous_gdp == 0:
            return 0, "لا يمكن الحساب (القيمة السابقة = 0)"
        growth = ((current_gdp - previous_gdp) / previous_gdp) * 100
        return growth, f"نمو: {growth:.2f}%"
    
    def calculate_cagr(self, begin_value, end_value, years):
        """معدل النمو السنوي المركب"""
        if begin_value <= 0 or years <= 0:
            return 0
        cagr = ((end_value / begin_value) ** (1 / years) - 1) * 100
        return cagr
    
    def compound_interest(self, principal, rate, years, n=12):
        """الفائدة المركبة"""
        amount = principal * (1 + rate / n) ** (n * years)
        return amount, amount - principal
    
    # ═══════════════════════════════════════════════════════
    # 2. التضخم والقوة الشرائية
    # ═══════════════════════════════════════════════════════
    
    def inflation_adjust(self, amount, inflation_rate, years):
        """تعديل المبلغ حسب التضخم"""
        adjusted = amount / ((1 + inflation_rate) ** years)
        return adjusted, amount - adjusted
    
    def real_return(self, nominal_return, inflation):
        """العائد الحقيقي (Fisher equation)"""
        real = ((1 + nominal_return) / (1 + inflation)) - 1
        return real * 100
    
    def purchasing_power(self, amount, inflation, years):
        """القوة الشرائية بعد سنوات"""
        return amount / ((1 + inflation) ** years)
    
    # ═══════════════════════════════════════════════════════
    # 3. تحليل الاستثمار
    # ═══════════════════════════════════════════════════════
    
    def roi(self, initial, final):
        """العائد على الاستثمار"""
        if initial == 0:
            return 0
        return ((final - initial) / initial) * 100
    
    def npv(self, cash_flows, discount_rate):
        """صافي القيمة الحالية"""
        npv = 0
        for t, cf in enumerate(cash_flows):
            npv += cf / ((1 + discount_rate) ** t)
        return npv
    
    def irr_approx(self, cash_flows, iterations=100):
        """معدل العائد الداخلي (تقريبي)"""
        if not cash_flows or cash_flows[0] >= 0:
            return None
        
        low, high = -0.99, 10.0
        for _ in range(iterations):
            mid = (low + high) / 2
            npv = sum(cf / ((1 + mid) ** t) for t, cf in enumerate(cash_flows))
            if abs(npv) < 1e-6:
                return mid * 100
            if npv > 0:
                low = mid
            else:
                high = mid
        return ((low + high) / 2) * 100
    
    def payback_period(self, initial, annual_cash_flow):
        """فترة الاسترداد"""
        if annual_cash_flow <= 0:
            return float('inf')
        return initial / annual_cash_flow
    
    # ═══════════════════════════════════════════════════════
    # 4. المخاطر والعوائد
    # ═══════════════════════════════════════════════════════
    
    def sharpe_ratio(self, returns, risk_free_rate=0.02):
        """نسبة شارب"""
        if len(returns) < 2:
            return 0
        avg_return = sum(returns) / len(returns)
        variance = sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
        std_dev = math.sqrt(variance)
        if std_dev == 0:
            return 0
        return (avg_return - risk_free_rate) / std_dev
    
    def volatility(self, returns):
        """التقلب (الانحراف المعياري)"""
        if len(returns) < 2:
            return 0
        avg = sum(returns) / len(returns)
        variance = sum((r - avg) ** 2 for r in returns) / (len(returns) - 1)
        return math.sqrt(variance)
    
    def max_drawdown(self, prices):
        """أقصى انخفاض"""
        if not prices:
            return 0
        peak = prices[0]
        max_dd = 0
        for price in prices:
            if price > peak:
                peak = price
            dd = (peak - price) / peak
            if dd > max_dd:
                max_dd = dd
        return max_dd * 100
    
    # ═══════════════════════════════════════════════════════
    # 5. تحليل الأسواق
    # ═══════════════════════════════════════════════════════
    
    def supply_demand_price(self, demand, supply, equilibrium_price=1.0):
        """سعر التوازن (نموذج مبسط)"""
        if supply == 0:
            return float('inf')
        return equilibrium_price * (demand / supply)
    
    def elasticity(self, p1, p2, q1, q2):
        """المرونة السعرية"""
        if (p1 + p2) == 0 or (q1 + q2) == 0:
            return 0
        return ((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2))
    
    def break_even_point(self, fixed_costs, price_per_unit, variable_cost_per_unit):
        """نقطة التعادل"""
        contribution = price_per_unit - variable_cost_per_unit
        if contribution <= 0:
            return float('inf')
        return fixed_costs / contribution
    
    # ═══════════════════════════════════════════════════════
    # 6. HITL
    # ═══════════════════════════════════════════════════════
    
    def await_mojeh_command(self, summary):
        print("\n" + "=" * 60)
        print(f"📢 [{self.agent_name}]")
        print(f"📝 {summary}")
        print("=" * 60)
        cmd = input("👤 [الموجه] موافقة؟ (yes/no): ")
        if cmd.strip().lower() == 'yes':
            print("🚀 تم الاعتماد.")
            return True
        print("🛑 تم التجميد.")
        return False


if __name__ == "__main__":
    agent = EconomyAgent()
    
    print("=" * 60)
    print("🎬 اختبار Economy Agent")
    print("=" * 60)
    
    growth, msg = agent.calculate_gdp_growth(1100, 1000)
    print(f"\n1️⃣ GDP نمو: {msg}")
    
    cagr = agent.calculate_cagr(100, 200, 10)
    print(f"2️⃣ CAGR: {cagr:.2f}%")
    
    amount, interest = agent.compound_interest(1000, 0.05, 10)
    print(f"3️⃣ فائدة مركبة: ${amount:.2f} (ربح: ${interest:.2f})")
    
    real = agent.real_return(0.08, 0.03)
    print(f"4️⃣ عائد حقيقي: {real:.2f}%")
    
    r = agent.roi(1000, 1500)
    print(f"5️⃣ ROI: {r:.2f}%")
    
    sr = agent.sharpe_ratio([0.05, 0.08, 0.06, 0.09, 0.07])
    print(f"6️⃣ Sharpe: {sr:.3f}")
    
    bep = agent.break_even_point(10000, 50, 30)
    print(f"7️⃣ Break-even: {bep:.0f} وحدة")
    
    agent.await_mojeh_command("اختبارات الاقتصاد — 7 حسابات")
