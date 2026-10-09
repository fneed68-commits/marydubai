from threading import Thread
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Bot is running"}

def start_server():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=start_server)
    t.daemon = True
    t.start()
    print("✅ Health check server started")
