from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 物件
# 將在 app.__init__.py 中與 Flask App 進行綁定 (db.init_app(app))
db = SQLAlchemy()
