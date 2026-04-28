import os
from flask import Flask
from app.models import db
from app.routes import register_blueprints

def create_app(test_config=None):
    # 初始化 Flask 應用，設定 instance_relative_config 讓資料庫可以放在 instance 資料夾中
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    
    if test_config is None:
        # 若有獨立的 config.py 可在此載入
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # 確保圖片上傳目錄存在
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # 將 db 綁定到 app
    db.init_app(app)
    
    # 在第一個請求前，確保所有資料表都已建立
    with app.app_context():
        # 若資料表已存在，create_all 不會覆蓋原有資料
        db.create_all()

    # 註冊所有 Blueprints (路由)
    register_blueprints(app)

    return app
