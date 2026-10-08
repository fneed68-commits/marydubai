#!/usr/bin/env python3
"""
MaryDubai-BlockchainGuard
وكيل تحليل البلوكشين والعملات المشفرة
مع تحكم بشري صارم (HITL)
"""
import hashlib
import math


class BlockchainAgent:
    def __init__(self):
        self.agent_name = "MaryDubai-BlockchainGuard"
        
        self.supported_chains = {
            "ethereum": {"symbol": "ETH", "decimals": 18, "chain_id": 1},
            "bnb":      {"symbol": "BNB", "decimals": 18, "chain_id": 56},
            "polygon":  {"symbol": "MATIC", "decimals": 18, "chain_id": 137},
            "bitcoin":  {"symbol": "BTC", "decimals": 8,  "chain_id": 0},
            "solana":   {"symbol": "SOL", "decimals": 9,  "chain_id": 101},
        }
    
    # ═══════════════════════════════════════════════════════
    # 1. التحقق من العناوين
    # ═══════════════════════════════════════════════════════
    
    def validate_eth_address(self, address):
        if not address or not address.startswith("0x"):
            return False, "يجب أن يبدأ بـ 0x"
        
        if len(address) != 42:
            return False, f"الطول يجب 42، الفعلي: {len(address)}"
        
        hex_part = address[2:]
        if not all(c in "0123456789abcdefABCDEF" for c in hex_part):
            return False, "يحتوي على أحرف غير hex"
        
        return True, "عنوان صحيح"
    
    def validate_btc_address(self, address):
        if not address:
            return False, "العنوان فارغ"
        
        if address.startswith("bc1"):
            if not 42 <= len(address) <= 62:
                return False, "طول Bech32 غير صحيح"
            return True, "عنوان Bech32 (SegWit)"
        
        if address[0] in "13":
            if not 26 <= len(address) <= 35:
                return False, "طول Legacy غير صحيح"
            return True, "عنوان Legacy/P2SH"
        
        return False, "صيغة غير معروفة"
    
    def validate_address(self, address, chain="ethereum"):
        print(f"\n🔍 [{self.agent_name}] التحقق من العنوان: {address[:10]}...")
        print(f"   🌐 الشبكة: {chain}")
        
        if chain.lower() in ["ethereum", "bnb", "polygon", "bsc"]:
            valid, msg = self.validate_eth_address(address)
        elif chain.lower() == "bitcoin":
            valid, msg = self.validate_btc_address(address)
        else:
            return False, f"شبكة غير مدعومة: {chain}"
        
        icon = "✅" if valid else "❌"
        print(f"   {icon} {msg}")
        return valid, msg
    
    # ═══════════════════════════════════════════════════════
    # 2. تحويل الوحدات
    # ═══════════════════════════════════════════════════════
    
    def wei_to_eth(self, wei):
        return wei / (10 ** 18)
    
    def eth_to_wei(self, eth):
        return int(eth * (10 ** 18))
    
    def to_human(self, amount, chain="ethereum"):
        if chain not in self.supported_chains:
            return amount
        
        decimals = self.supported_chains[chain]["decimals"]
        symbol = self.supported_chains[chain]["symbol"]
        
        human = amount / (10 ** decimals)
        return f"{human:.8f} {symbol}"
    
    # ═══════════════════════════════════════════════════════
    # 3. كشف المخاطر
    # ═══════════════════════════════════════════════════════
    
    def detect_scam_patterns(self, address, chain="ethereum"):
        risks = []
        
        if chain == "ethereum":
            hex_part = address[2:].lower() if address.startswith("0x") else address.lower()
            
            suspicious_patterns = [
                ("0000000000", "10 أصفار متتالية"),
                ("ffffffffff", "10 F متتالية"),
                ("deadbeef", "Deadbeef - تجريبي"),
                ("12345678", "12345678 - متسلسل"),
            ]
            
            for pattern, reason in suspicious_patterns:
                if pattern in hex_part:
                    risks.append(f"⚠️ نمط مشبوه: {reason}")
        
        if address.lower() == "0x0000000000000000000000000000000000000000":
            risks.append("🚨 عنوان صفري")
        
        return risks
    
    def analyze_transaction_risk(self, from_addr, to_addr, amount_eth):
        print(f"\n🔍 [{self.agent_name}] تحليل مخاطر المعاملة...")
        
        risks = []
        score = 100
        
        if amount_eth > 100:
            risks.append(f"🚨 مبلغ ضخم: {amount_eth} ETH")
            score -= 30
        elif amount_eth > 10:
            risks.append(f"⚠️ مبلغ كبير: {amount_eth} ETH")
            score -= 10
        
        if len(from_addr) < 42:
            risks.append("⚠️ عنوان المرسل غير مكتمل")
            score -= 20
        
        scam_patterns = self.detect_scam_patterns(to_addr)
        risks.extend(scam_patterns)
        score -= len(scam_patterns) * 15
        
        if 0 < amount_eth < 0.0001:
            risks.append("⚠️ Dust amount")
            score -= 5
        
        score = max(0, score)
        
        if score >= 80:
            level = "🟢 آمن"
        elif score >= 60:
            level = "🟡 انتبه"
        elif score >= 40:
            level = "🟠 خطر متوسط"
        else:
            level = "🔴 خطر عالي"
        
        print(f"   📊 {score}/100 — {level}")
        for r in risks:
            print(f"   {r}")
        
        return {"score": score, "level": level, "risks": risks}
    
    # ═══════════════════════════════════════════════════════
    # 4. تحليل المحفظة
    # ═══════════════════════════════════════════════════════
    
    def analyze_wallet(self, address, balance_eth=0, tx_count=0):
        print(f"\n🔍 [{self.agent_name}] تحليل المحفظة...")
        
        valid, msg = self.validate_address(address)
        if not valid:
            return {"error": msg}
        
        if balance_eth == 0:
            status = "🔴 فارغة"
            risk = "high"
        elif balance_eth < 0.01:
            status = "🟡 منخفض"
            risk = "medium"
        elif balance_eth < 1:
            status = "🟢 عادي"
            risk = "low"
        else:
            status = "💎 كبيرة"
            risk = "low"
        
        if tx_count == 0:
            activity = "🆕 لا نشاط"
        elif tx_count < 10:
            activity = "📊 قليل"
        elif tx_count < 100:
            activity = "📈 متوسط"
        else:
            activity = "🔥 عالي"
        
        print(f"   💰 {balance_eth} ETH | {status}")
        print(f"   {activity}")
        
        return {
            "address": address,
            "balance_eth": balance_eth,
            "status": status,
            "risk": risk,
            "activity": activity,
        }
    
    # ═══════════════════════════════════════════════════════
    # 5. حساب الغاز
    # ═══════════════════════════════════════════════════════
    
    def calculate_gas_cost(self, gas_limit, gas_price_gwei, eth_price_usd=3000):
        gas_price_eth = gas_price_gwei * 1e-9
        cost_eth = gas_limit * gas_price_eth
        cost_usd = cost_eth * eth_price_usd
        
        return {
            "gas_limit": gas_limit,
            "gas_price_gwei": gas_price_gwei,
            "cost_eth": cost_eth,
            "cost_usd": cost_usd,
        }
    
    # ═══════════════════════════════════════════════════════
    # 6. HITL
    # ═══════════════════════════════════════════════════════
    
    def await_mojeh_command(self, summary):
        print("\n" + "=" * 60)
        print(f"📢 [{self.agent_name}]")
        print(f"📝 {summary}")
        print("=" * 60)
        
        command = input("👤 [الموجه] موافقة؟ (yes/no): ")
        
        if command.strip().lower() == 'yes':
            print("🚀 تم الاعتماد.")
            return True
        print("🛑 تم التجميد.")
        return False


if __name__ == "__main__":
    agent = BlockchainAgent()
    
    print("=" * 60)
    print("🎬 اختبار Blockchain Agent")
    print("=" * 60)
    
    print("\n1️⃣ التحقق من العناوين:")
    agent.validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "ethereum")
    agent.validate_address("0xinvalid", "ethereum")
    agent.validate_address("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq", "bitcoin")
    
    print("\n2️⃣ تحويل الوحدات:")
    print(f"   1 ETH = {agent.eth_to_wei(1)} Wei")
    print(f"   10^18 Wei = {agent.wei_to_eth(10**18)} ETH")
    
    print("\n3️⃣ تحليل مخاطر:")
    agent.analyze_transaction_risk(
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
        "0x0000000000000000000000000000000000000000",
        5.0
    )
    
    print("\n4️⃣ حساب الغاز:")
    gas = agent.calculate_gas_cost(21000, 30, 3000)
    print(f"   {gas['cost_eth']:.6f} ETH (${gas['cost_usd']:.2f})")
    
    print("\n5️⃣ تحليل محفظة:")
    agent.analyze_wallet(
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
        balance_eth=1.5,
        tx_count=45
    )
    
    agent.await_mojeh_command("اختبارات Blockchain اكتملت")
