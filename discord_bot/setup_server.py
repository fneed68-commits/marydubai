#!/usr/bin/env python3
"""
MaryDubai Server Setup - إنشاء القنوات تلقائياً
"""
import discord
import os
import asyncio


# هيكل القنوات
CHANNELS = [
    # قسم المعلومات
    {"name": "📢-إعلانات", "topic": "أخبار MaryDubai والتحديثات", "type": "text"},
    {"name": "📜-قواعد", "topic": "قواعد السيرفر", "type": "text"},
    {"name": "👋-ترحيب", "topic": "رسائل الترحيب بالأعضاء", "type": "text"},
    
    # قسم المنتج
    {"name": "🎯-المنتج", "topic": "معلومات MaryDubai", "type": "text"},
    {"name": "💰-الأسعار", "topic": "الباقات", "type": "text"},
    {"name": "📥-التحميل", "topic": "خطوات التحميل", "type": "text"},
    
    # قسم المبيعات
    {"name": "🎉-sales", "topic": "إشعارات المبيعات", "type": "text"},
    {"name": "👥-عملاء", "topic": "قائمة المشترين", "type": "text"},
    
    # قسم الدعم
    {"name": "🆘-دعم-فني", "topic": "الدعم الفني", "type": "text"},
    {"name": "❓-أسئلة-شائعة", "topic": "الأسئلة المتكررة", "type": "text"},
    
    # قسم المجتمع
    {"name": "💬-عام", "topic": "محادثات عامة", "type": "text"},
    {"name": "🎨-نقاش", "topic": "نقاش حر", "type": "text"},
]


async def setup_guild(guild):
    """إعداد السيرفر"""
    print(f"🎯 إعداد: {guild.name}")
    
    # احذف القنوات الموجودة (اختياري)
    # for channel in guild.channels:
    #     try:
    #         await channel.delete()
    #     except:
    #         pass
    
    # أنشئ القنوات
    for ch in CHANNELS:
        try:
            await guild.create_text_channel(
                name=ch["name"],
                topic=ch["topic"],
                reason="MaryDubai Bot Setup"
            )
            print(f"   ✅ {ch['name']}")
        except discord.Forbidden:
            print(f"   ⚠️ لا توجد صلاحيات لإنشاء: {ch['name']}")
        except Exception as e:
            print(f"   ❌ خطأ في {ch['name']}: {e}")
    
    print(f"✅ تم إعداد {guild.name}")


async def main():
    """تشغيل الإعداد"""
    intents = discord.Intents.default()
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print("=" * 60)
        print(f"✅ البوت متصل: {client.user}")
        print("=" * 60)
        
        for guild in client.guilds:
            print(f"\n📋 إعداد السيرفر: {guild.name}")
            await setup_guild(guild)
        
        print("\n" + "=" * 60)
        print("✅ اكتمل الإعداد!")
        print("🛑 سيتم الإغلاق بعد 5 ثوان...")
        print("=" * 60)
        
        await asyncio.sleep(5)
        await client.close()
    
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("❌ DISCORD_BOT_TOKEN غير موجود")
        return
    
    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
