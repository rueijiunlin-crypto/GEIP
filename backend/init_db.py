#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料庫初始化腳本
匯入現有的JSON資料到SQLite資料庫
"""

import sys
import os
import json
from datetime import datetime
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_news_from_json():
    """從現有的news.json匯入資料"""
    try:
        # 讀取現有的news.json
        json_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data', 'news.json')
        if not os.path.exists(json_path):
            logger.warning(f"找不到檔案: {json_path}")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        logger.info(f"找到 {len(news_data)} 筆最新消息資料")
        
        # 檢查是否已有資料
        from app import app, db, NewsModel
        
        with app.app_context():
            existing_count = NewsModel.query.count()
            if existing_count > 0:
                logger.info(f"資料庫中已有 {existing_count} 筆資料，跳過匯入")
                return True
            
            # 匯入資料
            for item in news_data:
                try:
                    # 解析日期
                    date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                    
                    # 建立新聞物件
                    news = NewsModel(
                        title=item['title'],
                        date=date_obj,
                        link=item.get('link', ''),
                        status='published'
                    )
                    
                    db.session.add(news)
                    logger.info(f"匯入: {item['title']}")
                    
                except Exception as e:
                    logger.error(f"匯入失敗 {item.get('title', 'Unknown')}: {e}")
                    continue
            
            # 提交所有變更
            db.session.commit()
            logger.info(f"成功匯入 {len(news_data)} 筆最新消息")
            return True
            
    except Exception as e:
        logger.error(f"匯入過程發生錯誤: {e}")
        return False

def create_sample_data():
    """建立一些範例資料"""
    try:
        from app import app, db, NewsModel
        
        with app.app_context():
            # 檢查是否已有資料
            if NewsModel.query.count() > 0:
                logger.info("資料庫中已有資料，跳過建立範例資料")
                return True
            
            sample_news = [
                {
                    'title': '本學程開始接受 2026 年實習申請',
                    'date': '2025-09-10',
                    'content': '歡迎有興趣的同學踴躍申請，詳細資訊請參考申請流程頁面。',
                    'link': 'news_detail_20250910.html',
                    'status': 'published'
                },
                {
                    'title': '與某某公司簽訂合作協議，歡迎同學踴躍參與',
                    'date': '2025-09-05',
                    'content': '我們很高興宣布與某某公司建立新的合作關係，將為同學提供更多實習機會。',
                    'link': 'news_detail_20250905.html',
                    'status': 'published'
                },
                {
                    'title': '開學第一週課程表已公布，請至課程資訊查看',
                    'date': '2025-09-01',
                    'content': '新學期課程安排已確定，請同學們查看課程規劃表了解詳細資訊。',
                    'link': 'news_detail_20250901.html',
                    'status': 'published'
                }
            ]
            
            for item in sample_news:
                date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                news = NewsModel(
                    title=item['title'],
                    content=item['content'],
                    date=date_obj,
                    link=item['link'],
                    status=item['status']
                )
                db.session.add(news)
                logger.info(f"建立範例資料: {item['title']}")
            
            db.session.commit()
            logger.info("成功建立範例資料")
            return True
            
    except Exception as e:
        logger.error(f"建立範例資料失敗: {e}")
        return False

def main():
    """主函數"""
    logger.info("=== GEIP 資料庫初始化 ===")
    
    try:
        # 嘗試匯入現有資料
        logger.info("嘗試匯入現有JSON資料...")
        if not import_news_from_json():
            logger.info("匯入失敗，建立範例資料...")
            create_sample_data()
        
        # 顯示最終狀態
        from app import app, db, NewsModel
        
        with app.app_context():
            news_count = NewsModel.query.count()
            logger.info(f"資料庫初始化完成！")
            logger.info(f"目前共有 {news_count} 筆最新消息")
            
            # 顯示所有資料
            logger.info("資料庫內容:")
            all_news = NewsModel.query.order_by(NewsModel.date.desc()).all()
            for news in all_news:
                logger.info(f"  [{news.date}] {news.title}")
                
    except Exception as e:
        logger.error(f"初始化過程發生錯誤: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        logger.info("🎉 資料庫初始化成功！")
    else:
        logger.error("❌ 資料庫初始化失敗！")
        sys.exit(1)
