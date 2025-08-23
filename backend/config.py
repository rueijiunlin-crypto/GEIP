import os
from datetime import timedelta

class Config:
    """基礎設定類別"""
    # 基本設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'geip-secret-key-2025'
    
    # 資料庫設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///geip.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 應用程式設定
    NEWS_PER_PAGE = 10  # 每頁顯示的最新消息數量
    MAX_TITLE_LENGTH = 200  # 標題最大長度
    MAX_CONTENT_LENGTH = 5000  # 內容最大長度
    
    # 狀態選項
    NEWS_STATUS_OPTIONS = ['published', 'draft', 'archived']
    
    # 日期格式
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class DevelopmentConfig(Config):
    """開發環境設定"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生產環境設定"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """測試環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 設定字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
