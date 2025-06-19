import os
import sys

# ضمان إمكانية استيراد المجلدات العليا
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template
from flask_cors import CORS
from src.routes.analysis import analysis_bp

# إعداد التطبيق
app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf#FGSgvasgf$5$WGT"

# تفعيل CORS لجميع المصادر (يفضل تحديدها لاحقًا في الإنتاج)
CORS(app, origins="*")

# تسجيل المسارات (Blueprints)
# app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(analysis_bp, url_prefix="/api")

# مسار الواجهة الأمامية
@app.route("/")
def serve_frontend():
    return render_template("index.html")

# نقطة تشغيل الخادم
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=True)


