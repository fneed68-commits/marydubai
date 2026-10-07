"""
Shared Embeddings Module for MaryDubai Multi-Agent System
يدعم: Google Gemini API (عبر REST) | Local Hash (اختبار)
مع دعم Retry على Rate Limit
"""
import os
import json
import math
import time
import urllib.request
import urllib.error


class GeminiEmbedder:
    """Embedder using Google Gemini API via direct REST calls"""
    
    def __init__(self, api_key=None, model="gemini-embedding-001"):
        self.api_key = api_key or self._read_key()
        self.model = model
        self.max_retries = 3
        self.base_delay = 2  # ثواني
    
    def _read_key(self):
        key_file = os.path.expanduser("~/.marydubai/gemini_key.txt")
        if os.path.exists(key_file):
            with open(key_file) as f:
                return f.read().strip()
        return os.getenv("GEMINI_API_KEY")
    
    def embed(self, text):
        if not text or not text.strip():
            return [0.0] * 768
        
        if not self.api_key:
            raise RuntimeError("❌ GEMINI_API_KEY غير موجود")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:embedContent"
        
        payload = json.dumps({
            "content": {"parts": [{"text": text}]},
            "outputDimensionality": 768
        }).encode("utf-8")
        
        # محاولات مع تأخير متصاعد
        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": self.api_key,
                    },
                    method="POST",
                )
                
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data["embedding"]["values"]
                    
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = self.base_delay * (2 ** attempt)  # 2, 4, 8 ثواني
                    if attempt < self.max_retries - 1:
                        print(f"   ⏳ Rate limit — انتظار {wait}s (محاولة {attempt+1}/{self.max_retries})")
                        time.sleep(wait)
                    else:
                        raise RuntimeError(f"❌ تجاوز حد Gemini بعد {self.max_retries} محاولات")
                else:
                    body = e.read().decode("utf-8")
                    raise RuntimeError(f"❌ Gemini خطأ {e.code}: {body[:200]}")
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.base_delay)
                else:
                    raise RuntimeError(f"❌ فشل الاتصال: {e}")
        
        raise RuntimeError("❌ فشل الاتصال بـ Gemini")


class LocalHashEmbedder:
    """بديل محلي بدون إنترنت - للاختبار فقط"""
    
    def __init__(self, dim=384):
        self.dim = dim
    
    def embed(self, text):
        if not text:
            return [0.0] * self.dim
        import hashlib
        result = [0.0] * self.dim
        words = text.lower().split()
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            result[h % self.dim] += 1.0
        norm = math.sqrt(sum(x * x for x in result))
        if norm > 0:
            result = [x / norm for x in result]
        return result
