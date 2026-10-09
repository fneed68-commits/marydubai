import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# خادم ويب بسيط للرد على فحوصات Koyeb
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, format, *args):
        pass  # صامت

def run_health_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"✅ Health Check server listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # 1. شغّل خادم الفحص في الخلفية
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    # 2. شغّل البوت الرئيسي
    print("🚀 Starting MaryDubai Bot...")
    # استورد البوت هنا لضمان تشغيل الخادم أولاً
    import bot
    # الكود في bot.py يجب أن يستخدم bot.run(TOKEN) في النهاية
    # إذا كان يستخدم if __name__ == "__main__": فسيتم تنفيذه تلقائياً
