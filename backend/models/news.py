from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.database import format_date, format_datetime, sanitize_string

class News:
    """最新消息資料模型"""
    
    def __init__(self, db):
        self.db = db
        self.model = self._create_model()
    
    def _create_model(self):
        """建立最新消息資料表模型"""
        class NewsModel(self.db.Model):
            __tablename__ = 'news'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.String(200), nullable=False, index=True)
            content = self.db.Column(self.db.Text)
            date = self.db.Column(self.db.Date, nullable=False, index=True)
            link = self.db.Column(self.db.String(500))
            status = self.db.Column(self.db.String(20), default='published', index=True)
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            updated_at = self.db.Column(self.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            def __repr__(self):
                return f'<News {self.id}: {self.title}>'
            
            def to_dict(self):
                """轉換為字典格式"""
                return {
                    'id': self.id,
                    'title': self.title,
                    'content': self.content,
                    'date': format_date(self.date),
                    'link': self.link,
                    'status': self.status,
                    'created_at': format_datetime(self.created_at),
                    'updated_at': format_datetime(self.updated_at)
                }
            
            def to_public_dict(self):
                """轉換為公開字典格式（只包含已發布的內容）"""
                if self.status != 'published':
                    return None
                
                return {
                    'id': self.id,
                    'title': self.title,
                    'content': self.content,
                    'date': format_date(self.date),
                    'link': self.link,
                    'created_at': format_datetime(self.created_at)
                }
            
            def update_from_dict(self, data):
                """從字典更新資料"""
                if 'title' in data:
                    self.title = sanitize_string(data['title'], 200)
                if 'content' in data:
                    self.content = sanitize_string(data['content'], 5000)
                if 'date' in data:
                    self.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                if 'link' in data:
                    self.link = data['link'] if data['link'] else None
                if 'status' in data:
                    self.status = data['status']
                
                self.updated_at = datetime.utcnow()
        
        return NewsModel
    
    def get_model(self):
        """取得資料模型類別"""
        return self.model
    
    def create_table(self):
        """建立資料表"""
        self.model.__table__.create(self.db.engine, checkfirst=True)
    
    def drop_table(self):
        """刪除資料表"""
        self.model.__table__.drop(self.db.engine, checkfirst=True)
