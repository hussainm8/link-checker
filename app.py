from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # يسمح بالوصول من المتصفح بدون مشاكل CORS

@app.route("/check", methods=["GET"])
def check_url():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "يرجى إدخال الرابط عبر ?url="}), 400

    # التحقق من أن الرابط يبدأ بـ http:// أو https://
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "الرابط يجب أن يبدأ بـ http:// أو https://"}), 400

    try:
        start = time.time()
        try:
            # محاولة طلب HEAD أولاً
            response = requests.head(url, timeout=5, allow_redirects=True)
        except:
            # إذا فشل HEAD نستخدم GET
            response = requests.get(url, timeout=5, allow_redirects=True)

        elapsed = round(time.time() - start, 3)

        return jsonify({
            "reachable": True,
            "status": response.status_code,
            "finalUrl": response.url,
            "elapsed_seconds": elapsed
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "reachable": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    # تشغيل على جميع الشبكة المحلية (مثلاً 192.168.x.x) على المنفذ 5000
    app.run(host="127.0.0.1", port=5000, debug=True)

