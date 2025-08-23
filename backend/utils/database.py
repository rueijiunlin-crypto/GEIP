from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(app, db):
    """初始化資料庫"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("資料庫初始化成功")
            return True
    except Exception as e:
        logger.error(f"資料庫初始化失敗: {e}")
        return False

def get_pagination_info(page, per_page, total):
    """取得分頁資訊"""
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page * per_page < total else None
    }

def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """格式化日期時間"""
    if dt is None:
        return None
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            return dt
    return dt.strftime(format_str)

def format_date(dt, format_str='%Y-%m-%d'):
    """格式化日期"""
    if dt is None:
        return None
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, '%Y-%m-%d').date()
        except ValueError:
            return dt
    return dt.strftime(format_str)

def validate_date_string(date_str, format_str='%Y-%m-%d'):
    """驗證日期字串格式"""
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False

def sanitize_string(text, max_length=None):
    """清理字串（移除多餘空白、限制長度）"""
    if text is None:
        return None
    
    # 移除多餘空白
    cleaned = ' '.join(text.split())
    
    # 限制長度
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned
