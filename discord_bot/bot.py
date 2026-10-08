#!/usr/bin/env python3
"""
MaryDubai Discord Bot - النسخة الكاملة
17 أمر + /math group مع 7 sub-commands
"""
import os
import sys
import re
# إضافة المجلد الأب للمسار
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from discord import app_commands
from shared.cache import SmartCache

# ═══════════════════════════════════════════════════════
# الإعدادات الأساسية
# ═══════════════════════════════════════════════════════

PRODUCT = {
    "name": "MaryDubai Multi-Agent System",
    "version": "v1.0",
    "price_usd": 49,
    "price_lyd": 240,
    "payhip_url": "https://payhip.com/b/eP6gb",
    "store_url": "https://payhip.com/marydubai",
    "support_email": "fneed68@gmail.com",
}

WEBSITE_URL = "https://marydubai-agents.netlify.app"
DISCORD_URL = "https://discord.gg/HCb4ufeQDq"

COLORS = {
    "primary": 0x1a1a2e,
    "accent": 0x00d9ff,
    "success": 0x00ff88,
    "warning": 0xffaa00,
}

def clean_text(text):
    """ينظف النص من HTML والوسوم الزائدة"""
    if not text:
        return ""
    
    # إزالة وسوم HTML
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # إزالة CSS
    text = re.sub(r'[.#][a-zA-Z0-9_-]+\s*\{[^}]*\}', ' ', text)
    
    # إزالة JavaScript
    text = re.sub(r'<script.*?</script>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.DOTALL)
    
    # إزالة الفواصل الزائدة
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[{}\[\];]', ' ', text)
    
    # إزالة المسافات المتعددة
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


# إعداد البوت
intents = discord.Intents.default()
intents.guilds = True

# Cache للنصوص الثابتة
_cache = SmartCache(default_ttl=3600)  # ساعة واحدة

bot = commands.Bot(command_prefix="!", intents=intents)

# ═══════════════════════════════════════════════════════
# الأحداث
# ═══════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print("=" * 60)
    print(f"✅ البوت يعمل: {bot.user}")
    print(f"📡 في {len(bot.guilds)} سيرفر")
    print("=" * 60)
    try:
        synced = await bot.tree.sync()
        print(f"✅ تم مزامنة {len(synced)} أمر")
        for cmd in synced:
            print(f"   /{cmd.name}")
    except Exception as e:
        print(f"❌ خطأ في المزامنة: {e}")


# ═══════════════════════════════════════════════════════
# الأوامر الأساسية
# ═══════════════════════════════════════════════════════

@bot.tree.command(name="hello", description="اختبار البوت")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 مرحباً {interaction.user.mention}!")


@bot.tree.command(name="product", description="عرض تفاصيل المنتج")
async def product_info(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title=f"🎯 {PRODUCT['name']} {PRODUCT['version']}",
        description="نظام وكلاء ذكاء اصطناعي مع تحكم بشري صارم",
        color=COLORS["accent"],
    )
    embed.add_field(
        name="🤖 الوكلاء (7)",
        value=(
            "🔍 RAG - بحث ذكي\n"
            "⚖️ قانوني - تدقيق الامتثال\n"
            "🔄 كسر الحلقات - منع التكرار\n"
            "⏱️ الحواف الزمنية - فحص الحدود\n"
            "💰 مالي - تحليل الاستثمار\n"
            "🧮 رياضيات - حسابات دقيقة\n"
            "🛡️ أمن المحافظ - حماية الأصول"
        ),
        inline=False,
    )
    embed.add_field(
        name="✨ المميزات",
        value=(
            "✅ 7 وكلاء متخصصين\n"
            "✅ 74 اختبار ناجح (100%)\n"
            "✅ كود المصدر الكامل\n"
            "✅ رخصة تجارية\n"
            "✅ دعم 30 يوم"
        ),
        inline=False,
    )
    embed.add_field(
        name="💰 السعر",
        value=f"**${PRODUCT['price_usd']}** USD ≈ **{PRODUCT['price_lyd']}** د.ل",
        inline=False,
    )
    embed.add_field(
        name="🔗 الروابط",
        value=f"[🛒 الشراء]({PRODUCT['payhip_url']})\n[🌐 الموقع الرسمي]({WEBSITE_URL})",
        inline=False,
    )
    embed.set_footer(text="MaryDubai Multi-Agent System")
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="pricing", description="عرض الأسعار")
async def pricing(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="💰 باقات MaryDubai",
        color=COLORS["success"],
    )
    embed.add_field(name="🥉 Starter — $49", value="مطور واحد • دعم 30 يوم • تحديثات 6 أشهر", inline=False)
    embed.add_field(name="🥈 Professional — $149", value="حتى 5 مطورين • دعم 90 يوم • تحديثات سنة", inline=False)
    embed.add_field(name="🥇 Enterprise — $499", value="مطورين غير محدودين • White-Label • دعم سنة", inline=False)
    embed.add_field(name="🛒 للشراء", value=f"[اضغط هنا]({PRODUCT['payhip_url']})", inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="download", description="خطوات التحميل")
async def download(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="📥 خطوات التحميل",
        color=COLORS["primary"],
    )
    embed.add_field(
        name="📋 الخطوات",
        value=(
            f"1️⃣ افتح: {PRODUCT['payhip_url']}\n"
            "2️⃣ أدخل بريدك الإلكتروني\n"
            "3️⃣ حمّل الملف\n"
            "4️⃣ فك الضغط: `tar -xzf marydubai_v1.0_RELEASE.tar.gz`\n"
            "5️⃣ شغّل: `bash demo.sh`"
        ),
        inline=False,
    )
    embed.add_field(name="🆘 مشاكل؟", value=f"📧 {PRODUCT['support_email']}", inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="support", description="الدعم الفني")
async def support(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="🆘 الدعم الفني",
        description="نحن هنا لمساعدتك",
        color=COLORS["warning"],
    )
    embed.add_field(name="📧 البريد", value=PRODUCT["support_email"], inline=False)
    embed.add_field(name="💬 Discord", value=DISCORD_URL, inline=False)
    embed.add_field(name="⏱️ الاستجابة", value="24-48 ساعة", inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="buy", description="رابط الشراء المباشر")
async def buy_command(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="🛒 اشترِ MaryDubai الآن",
        description="اختر الباقة المناسبة",
        color=COLORS["success"],
    )
    embed.add_field(name="🥉 Starter", value="$49", inline=True)
    embed.add_field(name="🥈 Professional", value="$149", inline=True)
    embed.add_field(name="🥇 Enterprise", value="$499", inline=True)
    embed.add_field(name="🔗 رابط الشراء", value=f"[اضغط هنا]({PRODUCT['payhip_url']})", inline=False)
    embed.add_field(
        name="💳 طرق الدفع",
        value="YousrPay • Edfali • MobiCash • Moamalat",
        inline=False,
    )
    embed.set_footer(text="دفع آمن عبر DPay")
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="stats", description="إحصائيات المبيعات")
async def stats_command(interaction: discord.Interaction):
    await interaction.response.defer()
    import json
    from pathlib import Path
    import json as _json
    
    # مسار آمن ومقيّد
    ALLOWED_DIR = Path.home() / "termux_secops_project" / "sales"
    log_file = ALLOWED_DIR / "sales_log.json"
    
    # التحقق الصريح من الأمان
    try:
        resolved = log_file.resolve()
        if not str(resolved).startswith(str(ALLOWED_DIR.resolve())):
            raise ValueError("Path outside allowed directory")
    except (ValueError, OSError):
        sales_count = 0
        total_revenue = 0
    else:
        sales_count = 0
        total_revenue = 0
        if resolved.is_file():
            try:
                with open(resolved, 'r', encoding='utf-8') as f:
                    data = _json.load(f)
                    sales_count = len(data.get('sales', []))
                    total_revenue = data.get('total_revenue', 0)
            except (OSError, ValueError, KeyError):
                pass
    embed = discord.Embed(title="📊 إحصائيات MaryDubai", color=COLORS["warning"])
    embed.add_field(name="🛒 إجمالي المبيعات", value=f"**{sales_count}** عملية", inline=True)
    embed.add_field(name="💰 إجمالي الإيرادات", value=f"**${total_revenue}**", inline=True)
    avg = total_revenue / sales_count if sales_count > 0 else 0
    embed.add_field(name="📈 متوسط البيع", value=f"**${avg:.2f}**", inline=True)
    embed.set_footer(text="MaryDubai Analytics")
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="contact", description="معلومات الاتصال")
async def contact_command(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="📞 تواصل معنا", color=COLORS["accent"])
    embed.add_field(name="📧 البريد", value=PRODUCT["support_email"], inline=False)
    embed.add_field(name="💬 Discord", value=DISCORD_URL, inline=False)
    embed.add_field(name="🌐 الموقع", value=WEBSITE_URL, inline=False)
    embed.add_field(name="⏱️ الاستجابة", value="24-48 ساعة", inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="docs", description="التوثيق والروابط")
async def docs_command(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="📚 التوثيق والروابط", color=COLORS["primary"])
    embed.add_field(
        name="🚀 البدء السريع",
        value=(
            "```\n"
            "1. tar -xzf marydubai_v1.0.tar.gz\n"
            "2. cd termux_secops_project\n"
            "3. bash demo.sh\n"
            "4. python3 main.py --list\n"
            "```"
        ),
        inline=False,
    )
    embed.add_field(
        name="🧪 تشغيل الاختبارات",
        value="```python3 -m unittest discover -s tests -v```",
        inline=False,
    )
    embed.add_field(name="🔗 الروابط", value=f"[🌐 الموقع]({WEBSITE_URL})", inline=False)
    embed.add_field(name="🆘 مشاكل؟", value="استخدم `/contact` أو اكتب في #دعم-فني", inline=False)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="ask", description="اسأل عن MaryDubai (بحث ذكي مع Cache)")
@app_commands.describe(question="سؤالك عن المشروع أو المنتج")
async def ask_command(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    
    try:
        from shared.embeddings import GeminiEmbedder
        from shared.vector_store import SQLiteVectorStore
        from shared.cache import SmartCache
        
        # Cache عام (يبقى طوال عمر البوت)
        if not hasattr(ask_command, '_cache'):
            ask_command._cache = SmartCache(default_ttl=3600)
        
        cache = ask_command._cache
        
        # 1. افحص Cache
        cache_key = f"ask_{question}"
        cached = cache.get(cache_key)
        
        if cached is not None:
            # إجابة من Cache
            embed = discord.Embed(
                title="🔍 إجابة (من Cache ⚡)",
                description=f"**{question}**",
                color=COLORS["success"],
            )
            embed.add_field(
                name="📄 الإجابة",
                value=clean_text(cached["text"])[:1000] + ("..." if len(cached["text"]) > 1000 else ""),
                inline=False,
            )
            embed.add_field(name="📊 دقة المطابقة", value=f"{cached['score']:.2%}", inline=True)
            embed.add_field(name="📁 المصدر", value=cached["source"], inline=True)
            embed.set_footer(text="MaryDubai RAG • Cache Hit ⚡")
            await interaction.followup.send(embed=embed)
            return
        
        # 2. بحث فعلي
        store = SQLiteVectorStore(os.path.expanduser("~/termux_secops_project/rag_index.db"))
        if store.count() == 0:
            await interaction.followup.send("⚠️ قاعدة المعرفة فارغة.")
            return

        emb = GeminiEmbedder()
        query_vec = emb.embed(question)
        results = store.search(query_vec, k=3)

        if not results:
            await interaction.followup.send("❌ لم أجد إجابة.")
            return

        best = results[0]
        if best["score"] < 0.5:
            await interaction.followup.send(
                f"🤔 لم أجد إجابة دقيقة (أعلى تشابه: {best['score']:.2f}).\n"
                "جرّب صياغة مختلفة، أو استخدم `/contact`."
            )
            return

        # 3. خزّن في Cache
        cache_data = {
            "text": best["text"],
            "score": best["score"],
            "source": best["metadata"].get("filename", "؟"),
        }
        cache.set(cache_key, cache_data, ttl=3600)

        # 4. اعرض
        embed = discord.Embed(
            title="🔍 إجابة من قاعدة معرفة MaryDubai",
            description=f"**{question}**",
            color=COLORS["accent"],
        )
        embed.add_field(
            name="📄 الإجابة",
            value=clean_text(best["text"])[:1000] + ("..." if len(best["text"]) > 1000 else ""),
            inline=False,
        )
        embed.add_field(name="📊 دقة المطابقة", value=f"{best['score']:.2%}", inline=True)
        embed.add_field(name="📁 المصدر", value=cache_data["source"], inline=True)
        embed.set_footer(text="MaryDubai RAG • مدعوم بـ Gemini")
        await interaction.followup.send(embed=embed)
    
    except Exception as e:
        print(f"❌ خطأ في /ask: {e}")
        await interaction.followup.send(f"❌ حدث خطأ: {str(e)[:100]}")


# ═══════════════════════════════════════════════════════
# 🧮 أوامر الرياضيات والفيزياء (Group)
# ═══════════════════════════════════════════════════════

math_group = app_commands.Group(name="math", description="حسابات رياضية وفيزيائية وهندسية")


@math_group.command(name="force", description="F = m × a (قانون نيوتن الثاني)")
@app_commands.describe(mass="الكتلة بالكيلوغرام", acceleration="التسارع م/ث²")
async def math_force(interaction: discord.Interaction, mass: float, acceleration: float):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.newton_force(mass, acceleration)
    await interaction.response.send_message(
        f"⚡ **F = {result:.4f} N**\n\n`F = {mass} kg × {acceleration} m/s²`"
    )


@math_group.command(name="energy", description="E = mc² (طاقة الكتلة)")
@app_commands.describe(mass_kg="الكتلة بالكيلوغرام")
async def math_energy(interaction: discord.Interaction, mass_kg: float):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.mass_energy(mass_kg)
    await interaction.response.send_message(
        f"💥 **E = {result:.4e} J**\n\n`E = {mass_kg} kg × c²`"
    )


@math_group.command(name="photon", description="E = h·f (طاقة فوتون)")
@app_commands.describe(frequency_hz="التردد بالهرتز")
async def math_photon(interaction: discord.Interaction, frequency_hz: float):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.photon_energy(frequency_hz)
    await interaction.response.send_message(
        f"🔆 **E = {result:.4e} J**\n\n`E = h × {frequency_hz} Hz`"
    )


@math_group.command(name="series", description="المقاومة على التسلسل: R = R1 + R2")
@app_commands.describe(r1="المقاومة الأولى بالأوم", r2="المقاومة الثانية بالأوم")
async def math_resistor_series(interaction: discord.Interaction, r1: float, r2: float):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.resistor_series([r1, r2])

    embed = discord.Embed(title="🔌 مقاومة على التسلسل", color=0x00d9ff)
    embed.add_field(name="R1", value=f"{r1} Ω", inline=True)
    embed.add_field(name="R2", value=f"{r2} Ω", inline=True)
    embed.add_field(name="الصيغة", value="R = R1 + R2", inline=False)
    embed.add_field(name="✅ النتيجة", value=f"**R = {result:.4f} Ω**", inline=False)
    await interaction.response.send_message(embed=embed)


@math_group.command(name="parallel", description="المقاومة على التوازي: 1/R = 1/R1 + 1/R2")
@app_commands.describe(r1="المقاومة الأولى بالأوم", r2="المقاومة الثانية بالأوم")
async def math_resistor_parallel(interaction: discord.Interaction, r1: float, r2: float):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.resistor_parallel([r1, r2])

    embed = discord.Embed(title="🔌 مقاومة على التوازي", color=0x00d9ff)
    embed.add_field(name="R1", value=f"{r1} Ω", inline=True)
    embed.add_field(name="R2", value=f"{r2} Ω", inline=True)
    embed.add_field(name="الصيغة", value="1/R = 1/R1 + 1/R2", inline=False)
    embed.add_field(name="✅ النتيجة", value=f"**R = {result:.4f} Ω**", inline=False)
    await interaction.response.send_message(embed=embed)


@math_group.command(name="prime", description="هل العدد أولي؟")
@app_commands.describe(number="العدد للفحص")
async def math_prime(interaction: discord.Interaction, number: int):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    if number < 0:
        await interaction.response.send_message("❌ العدد يجب أن يكون موجباً")
        return
    is_prime = agent.is_prime(number)
    emoji = "✅" if is_prime else "❌"
    await interaction.response.send_message(
        f"{emoji} **{number}** {'أولي' if is_prime else 'ليس أولياً'}"
    )


@math_group.command(name="gcd", description="القاسم المشترك الأكبر (GCD)")
@app_commands.describe(a="العدد الأول", b="العدد الثاني")
async def math_gcd(interaction: discord.Interaction, a: int, b: int):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    result = agent.gcd(a, b)
    await interaction.response.send_message(f"🔢 **gcd({a}, {b}) = {result}**")


@math_group.command(name="modinv", description="المقلوب المعياري (أساس التشفير)")
@app_commands.describe(a="العدد", m="المعامل (Modulus)")
async def math_modinv(interaction: discord.Interaction, a: int, m: int):
    from math_physics_agent import MathPhysicsAgent
    agent = MathPhysicsAgent()
    try:
        result = agent.modular_inverse(a, m)
        await interaction.response.send_message(
            f"🔐 **{a}⁻¹ mod {m} = {result}**\n\n"
            f"تأكيد: ({a} × {result}) mod {m} = {(a * result) % m}"
        )
    except ValueError as e:
        await interaction.response.send_message(f"❌ {e}")


# تسجيل الـ Group
bot.tree.add_command(math_group)


# ═══════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("❌ DISCORD_BOT_TOKEN غير موجود")
        # لا نطبع أي مسار يحتوي على معلومات حساسة
        print("💡 شغّل setup_token.sh لإعداد التوكن")
        sys.exit(1)
    print("🚀 جاري تشغيل البوت...")
    bot.run(TOKEN)
