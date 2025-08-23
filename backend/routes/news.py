from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

# 設定日誌
logger = logging.getLogger(__name__)

# 建立藍圖
news_bp = Blueprint('news', __name__)

# 全域變數，將在app.py中設定
db = None
NewsModel = None
config = None

def init_news_routes(app_db, news_model, app_config):
    """初始化最新消息路由"""
    global db, NewsModel, config
    db = app_db
    NewsModel = news_model
    config = app_config

@news_bp.route('/news', methods=['GET'])
def get_news():
    """取得最新消息列表"""
    try:
        # 取得查詢參數
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', config.NEWS_PER_PAGE, type=int)
        status = request.args.get('status', 'published')
        search = request.args.get('search', '').strip()
        date_from = request.args.get('date_from', '').strip()
        date_to = request.args.get('date_to', '').strip()
        
        # 驗證參數
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = config.NEWS_PER_PAGE
        
        # 建立查詢
        query = NewsModel.query
        
        # 狀態篩選
        if status in config.NEWS_STATUS_OPTIONS:
            query = query.filter(NewsModel.status == status)
        
        # 搜尋功能
        if search:
            query = query.filter(
                db.or_(
                    NewsModel.title.contains(search),
                    NewsModel.content.contains(search)
                )
            )
        
        # 日期範圍篩選
        if date_from:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(NewsModel.date >= from_date)
            except ValueError:
                pass
        
        if date_to:
            try:
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(NewsModel.date <= to_date)
            except ValueError:
                pass
        
        # 排序（最新日期優先）
        query = query.order_by(NewsModel.date.desc(), NewsModel.created_at.desc())
        
        # 分頁
        total = query.count()
        news_list = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 準備回應資料
        data = []
        for news in news_list:
            if status == 'published':
                news_dict = news.to_public_dict()
                if news_dict:  # 只包含已發布的內容
                    data.append(news_dict)
            else:
                data.append(news.to_dict())
        
        # 分頁資訊
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_prev': page > 1,
            'has_next': page * per_page < total
        }
        
        return jsonify({
            'success': True,
            'data': data,
            'pagination': pagination,
            'message': f'成功取得 {len(data)} 筆最新消息'
        })
        
    except Exception as e:
        logger.error(f"取得最新消息失敗: {e}")
        return jsonify({
            'success': False,
            'error': '取得最新消息失敗',
            'message': str(e)
        }), 500

@news_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    """取得特定最新消息"""
    try:
        news = NewsModel.query.get(news_id)
        if not news:
            return jsonify({
                'success': False,
                'error': '最新消息不存在',
                'message': f'ID {news_id} 的最新消息不存在'
            }), 404
        
        # 根據狀態決定回傳格式
        if news.status == 'published':
            data = news.to_public_dict()
        else:
            data = news.to_dict()
        
        return jsonify({
            'success': True,
            'data': data,
            'message': '成功取得最新消息'
        })
        
    except Exception as e:
        logger.error(f"取得最新消息失敗: {e}")
        return jsonify({
            'success': False,
            'error': '取得最新消息失敗',
            'message': str(e)
        }), 500

@news_bp.route('/news', methods=['POST'])
def create_news():
    """建立新最新消息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '請求資料為空',
                'message': '請提供最新消息資料'
            }), 400
        
        # 驗證必要欄位
        if not data.get('title'):
            return jsonify({
                'success': False,
                'error': '標題為必要欄位',
                'message': '請提供最新消息標題'
            }), 400
        
        if not data.get('date'):
            return jsonify({
                'success': False,
                'error': '日期為必要欄位',
                'message': '請提供最新消息日期'
            }), 400
        
        # 驗證日期格式
        try:
            date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': '日期格式錯誤',
                'message': '日期格式應為 YYYY-MM-DD'
            }), 400
        
        # 驗證狀態
        status = data.get('status', 'published')
        if status not in config.NEWS_STATUS_OPTIONS:
            status = 'published'
        
        # 建立新消息
        new_news = NewsModel(
            title=data['title'].strip(),
            content=data.get('content', '').strip(),
            date=date_obj,
            link=data.get('link', '').strip() if data.get('link') else None,
            status=status
        )
        
        db.session.add(new_news)
        db.session.commit()
        
        logger.info(f"成功建立最新消息: {new_news.title}")
        
        return jsonify({
            'success': True,
            'data': new_news.to_dict(),
            'message': '最新消息建立成功'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"建立最新消息失敗: {e}")
        return jsonify({
            'success': False,
            'error': '建立最新消息失敗',
            'message': str(e)
        }), 500

@news_bp.route('/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    """更新最新消息"""
    try:
        news = NewsModel.query.get(news_id)
        if not news:
            return jsonify({
                'success': False,
                'error': '最新消息不存在',
                'message': f'ID {news_id} 的最新消息不存在'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '請求資料為空',
                'message': '請提供更新資料'
            }), 400
        
        # 更新資料
        news.update_from_dict(data)
        db.session.commit()
        
        logger.info(f"成功更新最新消息: {news.title}")
        
        return jsonify({
            'success': True,
            'data': news.to_dict(),
            'message': '最新消息更新成功'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新最新消息失敗: {e}")
        return jsonify({
            'success': False,
            'error': '更新最新消息失敗',
            'message': str(e)
        }), 500

@news_bp.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    """刪除最新消息"""
    try:
        news = NewsModel.query.get(news_id)
        if not news:
            return jsonify({
                'success': False,
                'error': '最新消息不存在',
                'message': f'ID {news_id} 的最新消息不存在'
            }), 404
        
        title = news.title
        db.session.delete(news)
        db.session.commit()
        
        logger.info(f"成功刪除最新消息: {title}")
        
        return jsonify({
            'success': True,
            'message': '最新消息刪除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"刪除最新消息失敗: {e}")
        return jsonify({
            'success': False,
            'error': '刪除最新消息失敗',
            'message': str(e)
        }), 500

@news_bp.route('/news/<int:news_id>/status', methods=['PATCH'])
def update_news_status(news_id):
    """更新最新消息狀態"""
    try:
        news = NewsModel.query.get(news_id)
        if not news:
            return jsonify({
                'success': False,
                'error': '最新消息不存在',
                'message': f'ID {news_id} 的最新消息不存在'
            }), 404
        
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status or new_status not in config.NEWS_STATUS_OPTIONS:
            return jsonify({
                'success': False,
                'error': '無效的狀態值',
                'message': f'狀態必須是以下之一: {", ".join(config.NEWS_STATUS_OPTIONS)}'
            }), 400
        
        old_status = news.status
        news.status = new_status
        news.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"最新消息狀態從 {old_status} 更新為 {new_status}: {news.title}")
        
        return jsonify({
            'success': True,
            'data': news.to_dict(),
            'message': f'最新消息狀態更新為 {new_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新最新消息狀態失敗: {e}")
        return jsonify({
            'success': False,
            'error': '更新最新消息狀態失敗',
            'message': str(e)
        }), 500
