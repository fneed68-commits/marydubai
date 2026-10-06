"""
Shared Embeddings Module for MaryDubai Multi-Agent System
يدعم: Google Gemini API (افتراضي) | Local Hash (اختبار)
"""
import os
import hashlib
import math


class GeminiEmbedder:
    """Embedder using Google Gemini API - للاستخدام الحقيقي"""
    
    def __init__(self, api_key=None, model="models/text-embedding-004"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self._client = None
    
    def _ensure_client(self):
        if self._client is None:
            if not self.api_key:
                raise RuntimeError(
                    "❌ GEMINI_API_KEY غير موجود. "
                    "صدّر المفتاح: export GEMINI_API_KEY=your_key"
                )
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
            except ImportError:
                raise RuntimeError("❌ pip install google-generativeai")
    
    def embed(self, text):
        if not text or not text.strip():
            return [0.0] * 768
        self._ensure_client()
        result = self._client.embed_content(
            model=self.model,
            content=text
        )
        return result["embedding"]


class LocalHashEmbedder:
    """بديل محلي بدون إنترنت - للاختبار فقط"""
    
    def __init__(self, dim=384):
        self.dim = dim
    
    def embed(self, text):
        if not text:
            return [0.0] * self.dim
        result = [0.0] * self.dim
        words = text.lower().split()
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            result[h % self.dim] += 1.0
        norm = math.sqrt(sum(x * x for x in result))
        if norm > 0:
            result = [x / norm for x in result]
        return result
