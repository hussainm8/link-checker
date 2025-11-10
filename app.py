from flask import Flask, request, jsonify,send_from_directory   # ← أضف send_from_directory هنا
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import time
import os

app = Flask(__name__)
CORS(app)
# ✅ تهيئة الـLimiter بدون تمرير app، ومع key_func داخل الـkwargs
limiter = Limiter(
    key_func=get_remote_address,
    app=app,                       # يُمرَّر هنا وليس موقعاً أوّلياً
    default_limits=["30 per minute"]
)
# --- نفس دالة الفحص السابقة مع تحسين بسيط ---
@app.route("/check", methods=["GET"])
@limiter.limit("30 per minute")          # ← مطبَّق هنا
def check_url():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "يرجى إدخال الرابط عبر ?url="}), 400
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "الرابط يجب أن يبدأ بـ http:// أو https://"}), 400

    try:
        start = time.time()
        try:      # نجرب HEAD أولاً
            r = requests.head(url, timeout=5, allow_redirects=True)
        except:   # إذا رفض الخادم HEAD نُحوّل لـ GET
            r = requests.get(url, timeout=5, allow_redirects=True)

        elapsed = round(time.time() - start, 3)
        return jsonify({
            "reachable": True,
            "status": r.status_code,
            "finalUrl": r.url,
            "elapsed_seconds": elapsed
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"reachable": False, "error": str(e)}), 500

@app.route('/')
def home():
    # ←←← اضعه هنا
    return send_from_directory('.', 'index.html')

# --- تشغيل عام/محلي بنفس الملف ---
if __name__ == "__main__":
    # المنفذ يُؤخذ من متغير بيئة PORT (توفِّره معظم منصّات النشر)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)   # اجعل debug=False في الإنتاج