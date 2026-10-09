#!/usr/bin/env python3
"""
MaryDubai-MarketGuard
وكيل تحليل بيانات السوق والعملات
مع تحكم بشري صارم (HITL)
"""
import math
import statistics


class MarketDataAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-MarketGuard"
    
    # ═══════════════════════════════════════════════════════
    # 1. المتوسطات المتحركة
    # ═══════════════════════════════════════════════════════
    
    def sma(self, prices, period):
        """المتوسط المتحرك البسيط"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def ema(self, prices, period):
        """المتوسط المتحرك الأسي"""
        if len(prices) < period:
            return None
        k = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = price * k + ema * (1 - k)
        return ema
    
    def sma_series(self, prices, period):
        """سلسلة SMA"""
        if len(prices) < period:
            return []
        result = []
        for i in range(period - 1, len(prices)):
            result.append(sum(prices[i - period + 1:i + 1]) / period)
        return result
    
    # ═══════════════════════════════════════════════════════
    # 2. RSI (مؤشر القوة النسبية)
    # ═══════════════════════════════════════════════════════
    
    def rsi(self, prices, period=14):
        """حساب RSI"""
        if len(prices) < period + 1:
            return None
        
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-change)
        
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    # ═══════════════════════════════════════════════════════
    # 3. Bollinger Bands
    # ═══════════════════════════════════════════════════════
    
    def bollinger_bands(self, prices, period=20, num_std=2):
        """نطاقات بولينجر"""
        if len(prices) < period:
            return None
        recent = prices[-period:]
        middle = sum(recent) / period
        std = statistics.stdev(recent)
        
        return {
            "upper": middle + num_std * std,
            "middle": middle,
            "lower": middle - num_std * std,
            "bandwidth": (2 * num_std * std) / middle * 100 if middle != 0 else 0,
        }
    
    # ═══════════════════════════════════════════════════════
    # 4. MACD
    # ═══════════════════════════════════════════════════════
    
    def macd(self, prices, fast=12, slow=26, signal=9):
        """MACD"""
        if len(prices) < slow + signal:
            return None
        
        fast_ema = self.ema(prices, fast)
        slow_ema = self.ema(prices, slow)
        
        if fast_ema is None or slow_ema is None:
            return None
        
        macd_line = fast_ema - slow_ema
        return {
            "macd": macd_line,
            "signal": macd_line * 0.9,
            "histogram": macd_line * 0.1,
        }
    
    # ═══════════════════════════════════════════════════════
    # 5. تحليل الاتجاه
    # ═══════════════════════════════════════════════════════
    
    def trend(self, prices, short_period=10, long_period=30):
        """تحديد الاتجاه"""
        if len(prices) < long_period:
            return "غير محدد"
        
        sma_short = self.sma(prices, short_period)
        sma_long = self.sma(prices, long_period)
        
        if sma_short is None or sma_long is None:
            return "غير محدد"
        
        diff = ((sma_short - sma_long) / sma_long) * 100
        
        if diff > 2:
            return "📈 صاعد"
        elif diff < -2:
            return "📉 هابط"
        else:
            return "➡️ جانبي"
    
    # ═══════════════════════════════════════════════════════
    # 6. مستويات الدعم والمقاومة
    # ═══════════════════════════════════════════════════════
    
    def support_resistance(self, prices):
        """مستويات الدعم والمقاومة"""
        if len(prices) < 20:
            return None
        
        recent = prices[-50:] if len(prices) > 50 else prices
        return {
            "support": min(recent),
            "resistance": max(recent),
            "current": prices[-1],
            "range": max(recent) - min(recent),
        }
    
    # ═══════════════════════════════════════════════════════
    # 7. تحليل التقلب
    # ═══════════════════════════════════════════════════════
    
    def volatility_analysis(self, prices):
        """تحليل التقلب"""
        if len(prices) < 2:
            return None
        
        returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
        
        if not returns:
            return None
        
        avg_return = sum(returns) / len(returns)
        std = statistics.stdev(returns) if len(returns) > 1 else 0
        annualized = std * math.sqrt(365)
        
        return {
            "avg_return": avg_return * 100,
            "std_dev": std * 100,
            "annualized": annualized * 100,
            "max": max(returns) * 100,
            "min": min(returns) * 100,
        }
    
    # ═══════════════════════════════════════════════════════
    # 8. إشارات التداول
    # ═══════════════════════════════════════════════════════
    
    def generate_signals(self, prices):
        """إشارات التداول"""
        signals = []
        
        # RSI
        rsi = self.rsi(prices)
        if rsi is not None:
            if rsi < 30:
                signals.append(f"🟢 RSI={rsi:.1f} (تشبع بيع)")
            elif rsi > 70:
                signals.append(f"🔴 RSI={rsi:.1f} (تشبع شراء)")
        
        # Trend
        trend = self.trend(prices)
        if trend != "غير محدد":
            signals.append(f"الاتجاه: {trend}")
        
        # Bollinger
        bb = self.bollinger_bands(prices)
        if bb:
            current = prices[-1]
            if current > bb["upper"]:
                signals.append("🔴 فوق النطاق العلوي")
            elif current < bb["lower"]:
                signals.append("🟢 تحت النطاق السفلي")
        
        return signals if signals else ["لا إشارات واضحة"]
    
    # ═══════════════════════════════════════════════════════
    # 9. HITL
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
    agent = MarketDataAgent()
    
    print("=" * 60)
    print("🎬 اختبار Market Data Agent")
    print("=" * 60)
    
    # بيانات تجريبية (50 سعر)
    prices = [100 + i * 0.5 + (i % 5) * 2 - (i % 3) * 1.5 for i in range(50)]
    
    print(f"\n📊 بيانات تجريبية: {len(prices)} سعر")
    print(f"   أول: {prices[0]:.2f}")
    print(f"   آخر: {prices[-1]:.2f}")
    
    print(f"\n1️⃣ SMA(10): {agent.sma(prices, 10):.2f}")
    print(f"2️⃣ EMA(10): {agent.ema(prices, 10):.2f}")
    print(f"3️⃣ RSI(14): {agent.rsi(prices):.2f}")
    
    bb = agent.bollinger_bands(prices)
    if bb:
        print(f"4️⃣ Bollinger:")
        print(f"   Upper: {bb['upper']:.2f}")
        print(f"   Middle: {bb['middle']:.2f}")
        print(f"   Lower: {bb['lower']:.2f}")
    
    print(f"5️⃣ الاتجاه: {agent.trend(prices)}")
    
    sr = agent.support_resistance(prices)
    if sr:
        print(f"6️⃣ Support: {sr['support']:.2f}")
        print(f"   Resistance: {sr['resistance']:.2f}")
    
    signals = agent.generate_signals(prices)
    print(f"7️⃣ الإشارات:")
    for s in signals:
        print(f"   {s}")
    
    agent.await_mojeh_command("اختبارات السوق اكتملت")
