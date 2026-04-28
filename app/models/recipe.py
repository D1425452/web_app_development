from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models import db

# 定義多對多中介表：食譜_標籤
recipe_tag = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    is_favorite = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 定義與 Tag 的多對多關聯
    tags = db.relationship('Tag', secondary=recipe_tag, lazy='subquery',
                           backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return f'<Recipe {self.title}>'

    # --- CRUD 方法 ---

    @classmethod
    def get_all(cls):
        """
        取得所有食譜，依建立時間降冪排序。
        回傳: list of Recipe objects 或空列表
        """
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error fetching all recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        透過 ID 取得特定食譜。
        參數: recipe_id (int)
        回傳: Recipe object 或 None
        """
        try:
            return cls.query.get(recipe_id)
        except SQLAlchemyError as e:
            print(f"Error fetching recipe {recipe_id}: {e}")
            return None

    def create(self):
        """
        新增食譜至資料庫。
        回傳: self (成功) 或 None (失敗)
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None

    def update(self, **kwargs):
        """
        更新食譜內容。
        參數: kwargs (需要更新的欄位與值)
        回傳: self (成功) 或 None (失敗)
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating recipe {self.id}: {e}")
            return None

    def delete(self):
        """
        從資料庫刪除食譜。
        回傳: True (成功) 或 False (失敗)
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting recipe {self.id}: {e}")
            return False
