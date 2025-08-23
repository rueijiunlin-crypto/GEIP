from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import logging
from datetime import datetime

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 建立Flask應用程式
app = Flask(__name__)

# 載入設定
config_name = os.environ.get('FLASK_ENV', 'development')
from config import config
app.config.from_object(config[config_name])

# 初始化資料庫
db = SQLAlchemy(app)

# 啟用CORS
CORS(app)

# 初始化最新消息模型
from models.news import News
news_model = News(db)
NewsModel = news_model.get_model()

# 管理後台首頁
@app.route('/')
def admin_home():
    """管理後台首頁"""
    try:
        # 取得統計資訊
        total_news = NewsModel.query.count()
        published_news = NewsModel.query.filter_by(status='published').count()
        draft_news = NewsModel.query.filter_by(status='draft').count()
        archived_news = NewsModel.query.filter_by(status='archived').count()
        
        # 取得最新5筆消息
        latest_news = NewsModel.query.order_by(NewsModel.created_at.desc()).limit(5).all()
        
        return render_template('admin_home.html', 
                             total_news=total_news,
                             published_news=published_news,
                             draft_news=draft_news,
                             archived_news=archived_news,
                             latest_news=latest_news)
    except Exception as e:
        logger.error(f"管理後台首頁錯誤: {e}")
        flash('載入首頁時發生錯誤', 'error')
        return render_template('admin_home.html')

# 最新消息管理
@app.route('/news')
def news_list():
    """最新消息列表頁面"""
    try:
        # 取得查詢參數
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        search = request.args.get('search', '')
        
        # 建立查詢
        query = NewsModel.query
        
        # 狀態篩選
        if status and status in config[config_name].NEWS_STATUS_OPTIONS:
            query = query.filter(NewsModel.status == status)
        
        # 搜尋功能
        if search:
            query = query.filter(
                db.or_(
                    NewsModel.title.contains(search),
                    NewsModel.content.contains(search)
                )
            )
        
        # 排序（最新日期優先）
        query = query.order_by(NewsModel.date.desc(), NewsModel.created_at.desc())
        
        # 分頁
        total = query.count()
        news_list = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # 分頁資訊
        total_pages = (total + per_page - 1) // per_page
        
        return render_template('news_list.html',
                             news_list=news_list,
                             page=page,
                             per_page=per_page,
                             total=total,
                             total_pages=total_pages,
                             status=status,
                             search=search,
                             status_options=config[config_name].NEWS_STATUS_OPTIONS)
    except Exception as e:
        logger.error(f"最新消息列表錯誤: {e}")
        flash('載入最新消息列表時發生錯誤', 'error')
        return render_template('news_list.html')

@app.route('/news/new', methods=['GET', 'POST'])
def news_new():
    """新增最新消息頁面"""
    if request.method == 'POST':
        try:
            # 取得表單資料
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            date = request.form.get('date', '').strip()
            link = request.form.get('link', '').strip()
            status = request.form.get('status', 'published')
            
            # 驗證資料
            if not title:
                flash('標題為必要欄位', 'error')
                return render_template('news_form.html', 
                                   title=title, content=content, date=date, 
                                   link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            if not date:
                flash('日期為必要欄位', 'error')
                return render_template('news_form.html', 
                                   title=title, content=content, date=date, 
                                   link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            # 驗證日期格式
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                flash('日期格式錯誤，應為 YYYY-MM-DD', 'error')
                return render_template('news_form.html', 
                                   title=title, content=content, date=date, 
                                   link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            # 建立新消息
            new_news = NewsModel(
                title=title,
                content=content,
                date=date_obj,
                link=link if link else None,
                status=status
            )
            
            db.session.add(new_news)
            db.session.commit()
            
            flash(f'成功新增最新消息：{title}', 'success')
            return redirect(url_for('news_list'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"新增最新消息錯誤: {e}")
            flash('新增最新消息時發生錯誤', 'error')
            return render_template('news_form.html', 
                               title=title, content=content, date=date, 
                               link=link, status=status, 
                               status_options=config[config_name].NEWS_STATUS_OPTIONS)
    
    # GET 請求，顯示表單
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('news_form.html', 
                         title='', content='', date=today, 
                         link='', status='published', 
                         status_options=config[config_name].NEWS_STATUS_OPTIONS)

@app.route('/news/<int:news_id>/edit', methods=['GET', 'POST'])
def news_edit(news_id):
    """編輯最新消息頁面"""
    try:
        news = NewsModel.query.get_or_404(news_id)
        
        if request.method == 'POST':
            # 取得表單資料
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            date = request.form.get('date', '').strip()
            link = request.form.get('link', '').strip()
            status = request.form.get('status', 'published')
            
            # 驗證資料
            if not title:
                flash('標題為必要欄位', 'error')
                return render_template('news_form.html', 
                                   news=news, title=title, content=content, 
                                   date=date, link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            if not date:
                flash('日期為必要欄位', 'error')
                return render_template('news_form.html', 
                                   news=news, title=title, content=content, 
                                   date=date, link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            # 驗證日期格式
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                flash('日期格式錯誤，應為 YYYY-MM-DD', 'error')
                return render_template('news_form.html', 
                                   news=news, title=title, content=content, 
                                   date=date, link=link, status=status, 
                                   status_options=config[config_name].NEWS_STATUS_OPTIONS)
            
            # 更新資料
            news.title = title
            news.content = content
            news.date = date_obj
            news.link = link if link else None
            news.status = status
            news.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'成功更新最新消息：{title}', 'success')
            return redirect(url_for('news_list'))
        
        # GET 請求，顯示編輯表單
        return render_template('news_form.html', 
                             news=news, title=news.title, content=news.content, 
                             date=news.date.strftime('%Y-%m-%d'), 
                             link=news.link or '', status=news.status, 
                             status_options=config[config_name].NEWS_STATUS_OPTIONS)
        
    except Exception as e:
        logger.error(f"編輯最新消息錯誤: {e}")
        flash('編輯最新消息時發生錯誤', 'error')
        return redirect(url_for('news_list'))

@app.route('/news/<int:news_id>/delete', methods=['POST'])
def news_delete(news_id):
    """刪除最新消息"""
    try:
        news = NewsModel.query.get_or_404(news_id)
        title = news.title
        
        db.session.delete(news)
        db.session.commit()
        
        flash(f'成功刪除最新消息：{title}', 'success')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"刪除最新消息錯誤: {e}")
        flash('刪除最新消息時發生錯誤', 'error')
    
    return redirect(url_for('news_list'))

@app.route('/news/<int:news_id>/status', methods=['POST'])
def news_status(news_id):
    """更新最新消息狀態"""
    try:
        news = NewsModel.query.get_or_404(news_id)
        new_status = request.form.get('status')
        
        if new_status and new_status in config[config_name].NEWS_STATUS_OPTIONS:
            old_status = news.status
            news.status = new_status
            news.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'成功更新狀態：{old_status} → {new_status}', 'success')
        else:
            flash('無效的狀態值', 'error')
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新狀態錯誤: {e}")
        flash('更新狀態時發生錯誤', 'error')
    
    return redirect(url_for('news_list'))

# 錯誤處理
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='頁面不存在', message='請求的資源不存在'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error='伺服器內部錯誤', message='請稍後再試'), 500

if __name__ == '__main__':
    logger.info(f"啟動GEIP管理後台 (環境: {config_name})")
    
    # 建立資料表
    with app.app_context():
        db.create_all()
        logger.info("資料庫初始化完成")
    
    # 啟動服務
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5001
    )
