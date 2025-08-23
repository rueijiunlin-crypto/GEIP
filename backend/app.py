from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 建立Flask應用程式
app = Flask(__name__)

# 載入設定
config_name = os.environ.get('FLASK_ENV', 'development')
from config import config
app.config.from_object(config[config_name])

# 初始化資料庫
db = SQLAlchemy(app)

# 啟用CORS - 明確指定允許的來源
CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500', 'http://127.0.0.1:3000', 'http://localhost:3000'])

# 初始化最新消息模型
from models.news import News
news_model = News(db)
NewsModel = news_model.get_model()

# 初始化路由
from routes.news import init_news_routes, news_bp
# 傳遞設定物件而不是app.config
init_news_routes(db, NewsModel, config[config_name])
app.register_blueprint(news_bp, url_prefix='/api')

# 測試端點
@app.route('/api/test', methods=['GET'])
def test():
    """測試API是否正常運作"""
    return jsonify({
        'success': True,
        'message': 'GEIP後端API運作正常',
        'version': '1.0.0',
        'environment': config_name
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    try:
        # 檢查資料庫連線 - 使用text()包裝SQL語句
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'success': True,
        'status': 'running',
        'database': db_status,
        'timestamp': '2025-01-23T12:00:00Z'
    })

# 錯誤處理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '頁面不存在',
        'message': '請求的資源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': '伺服器內部錯誤',
        'message': '請稍後再試'
    }), 500

# 應用程式啟動事件 - 使用新的方式
def create_tables():
    """建立資料表"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("資料表建立完成")
    except Exception as e:
        logger.error(f"建立資料表失敗: {e}")

# 在應用程式啟動時建立資料表
with app.app_context():
    create_tables()

if __name__ == '__main__':
    logger.info(f"啟動GEIP後端API服務 (環境: {config_name})")
    logger.info(f"資料庫: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 建立資料表
    with app.app_context():
        db.create_all()
        logger.info("資料庫初始化完成")
    
    # 啟動服務
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000
    )
