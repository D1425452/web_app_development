from sqlalchemy.exc import SQLAlchemyError
from app.models import db

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'

    # --- CRUD 方法 ---

    @classmethod
    def get_all(cls):
        """
        取得所有標籤。
        回傳: list of Tag objects 或空列表
        """
        try:
            return cls.query.all()
        except SQLAlchemyError as e:
            print(f"Error fetching all tags: {e}")
            return []

    @classmethod
    def get_by_id(cls, tag_id):
        """
        透過 ID 取得特定標籤。
        參數: tag_id (int)
        回傳: Tag object 或 None
        """
        try:
            return cls.query.get(tag_id)
        except SQLAlchemyError as e:
            print(f"Error fetching tag {tag_id}: {e}")
            return None

    @classmethod
    def get_or_create(cls, name):
        """
        透過名稱尋找標籤，若不存在則建立。
        參數: name (str)
        回傳: Tag object 或 None
        """
        try:
            tag = cls.query.filter_by(name=name).first()
            if not tag:
                tag = cls(name=name)
                db.session.add(tag)
                db.session.commit()
            return tag
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error getting/creating tag {name}: {e}")
            return None

    def create(self):
        """
        新增標籤至資料庫。
        回傳: self (成功) 或 None (失敗)
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating tag: {e}")
            return None

    def update(self, name):
        """
        更新標籤名稱。
        參數: name (str)
        回傳: self (成功) 或 None (失敗)
        """
        try:
            self.name = name
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating tag {self.id}: {e}")
            return None

    def delete(self):
        """
        從資料庫刪除標籤。
        回傳: True (成功) 或 False (失敗)
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting tag {self.id}: {e}")
            return False
