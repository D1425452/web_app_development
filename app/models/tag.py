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
        """取得所有標籤"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, tag_id):
        """透過 ID 取得特定標籤"""
        return cls.query.get(tag_id)

    def create(self):
        """新增標籤至資料庫"""
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, name):
        """更新標籤名稱"""
        self.name = name
        db.session.commit()
        return self

    def delete(self):
        """從資料庫刪除標籤"""
        db.session.delete(self)
        db.session.commit()
