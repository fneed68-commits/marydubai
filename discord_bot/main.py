#!/usr/bin/env python3
import os, sys, threading, time, json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="MaryDubai Unified")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

LANDING = """<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MaryDubai Server</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,sans-serif;background:linear-gradient(135deg,#0a0a1f,#1a1a2e);color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:rgba(26,26,46,.95);padding:3rem;border-radius:24px;box-shadow:0 20px 60px rgba(0,217,255,.15);border:1px solid rgba(0,217,255,.2);max-width:560px;text-align:center}
h1{background:linear-gradient(135deg,#00d9ff,#00ff88);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.2rem;margin-bottom:1rem}
.badge{background:linear-gradient(135deg,#00ff88,#00d9ff);color:#0a0a1f;padding:8px 20px;border-radius:30px;font-weight:bold;display:inline-block;margin:1rem 0}
p{color:#aaa;line-height:1.8}
.links{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:2rem}
.links a{display:block;padding:12px;background:rgba(0,217,255,.1);border:1px solid rgba(0,217,255,.3);border-radius:12px;color:#00d9ff;text-decoration:none}
.links a:hover{background:rgba(0,217,255,.2)}
.info{margin-top:2rem;padding-top:1.5rem;border-top:1px solid rgba(0,217,255,.2);font-size:.85rem;color:#666}
</style></head><body>
<div class="card">
<h1>🚀 MaryDubai Server</h1>
<div class="badge">يعمل 24/7 على Koyeb</div>
<p>خادم موحد: بوت + ويب + AI</p>
<div class="links">
<a href="/docs">📖 API</a>
<a href="/health">💚 Health</a>
<a href="/api/stats">📊 Stats</a>
<a href="/api/ask?q=مرحبا">🤖 اسأل</a>
</div>
<div class="info">Powered by MaryDubai Unified v1.0</div>
</div></body></html>"""

START_TIME = time.time()
BOT_RUNNING = False

@app.get("/", response_class=HTMLResponse)
async def home(): return LANDING

@app.get("/health")
async def health(): return {"status":"ok","service":"marydubai-unified","version":"1.0"}

@app.get("/api/stats")
async def stats():
    import shutil
    d = shutil.disk_usage("/")
    return {"uptime":int(time.time()-START_TIME),"disk_free_gb":round(d.free/1e9,2),"bot_running":BOT_RUNNING}

@app.get("/api/ask")
async def ask(q: str):
    if not q or len(q) > 500: raise HTTPException(400,"Invalid question")
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        kf = os.path.expanduser("~/.marydubai/gemini_key.txt")
        if os.path.exists(kf): key = open(kf).read().strip()
    if not key: raise HTTPException(500,"Gemini key missing")
    try:
        import urllib.request
        model = os.getenv("GEMINI_MODEL","gemini-3.8-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {"contents":[{"parts":[{"text":q}]}]}
        req = urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            data = json.loads(r.read())
        return {"question":q,"answer":data["candidates"][0]["content"]["parts"][0]["text"],"model":model}
    except Exception as e: raise HTTPException(500,str(e)[:200])

def run_bot():
    global BOT_RUNNING
    try:
        BOT_RUNNING = True
        print("🤖 Starting Discord bot...")
        import bot
    except Exception as e:
        print(f"❌ Bot error: {e}")
        BOT_RUNNING = False

def start_web():
    port = int(os.getenv("PORT","8000"))
    uvicorn.run(app,host="0.0.0.0",port=port,log_level="warning")

if __name__ == "__main__":
    print("═"*50)
    print("🚀 MaryDubai Unified Server")
    print("═"*50)
    threading.Thread(target=start_web,daemon=True).start()
    time.sleep(2)
    threading.Thread(target=run_bot,daemon=True).start()
    print("✅ Web + Bot running")
    try:
        while True: time.sleep(60)
    except KeyboardInterrupt: print("\n🛑 Shutdown")
