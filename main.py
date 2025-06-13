import os
import sys

# ضمان إمكانية استيراد المجلدات العليا
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.user import user_bp
from src.routes.analysis import analysis_bp
# من الممكن تمكين قاعدة البيانات لاحقًا عند الحاجة
# from src.models.user import db

# إعداد التطبيق
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# تفعيل CORS لجميع المصادر (يفضل تحديدها لاحقًا في الإنتاج)
CORS(app, origins="*")

# تسجيل المسارات (Blueprints)
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(analysis_bp, url_prefix='/api')

# إعداد قاعدة البيانات (اختياري، يمكن تفعيله عند الحاجة)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# خدمة ملفات static و index.html
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, 'index.html')
    
    return "index.html not found", 404

# نقطة تشغيل الخادم
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




