#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試最新消息API的腳本
"""

import requests
import json
from datetime import datetime
import time

# API基礎URL
BASE_URL = 'http://localhost:5000/api'

def test_api_connection():
    """測試API連線"""
    print("=== 測試API連線 ===")
    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API連線成功: {data['message']}")
            print(f"   版本: {data['version']}")
            print(f"   環境: {data['environment']}")
            return True
        else:
            print(f"❌ API連線失敗: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到API，請確認後端服務是否正在運行")
        return False
    except Exception as e:
        print(f"❌ 連線測試發生錯誤: {e}")
        return False

def test_health_check():
    """測試健康檢查"""
    print("\n=== 測試健康檢查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康檢查成功")
            print(f"   狀態: {data['status']}")
            print(f"   資料庫: {data['database']}")
            return True
        else:
            print(f"❌ 健康檢查失敗: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康檢查測試失敗: {e}")
        return False

def test_get_news():
    """測試取得最新消息"""
    print("\n=== 測試取得最新消息 ===")
    try:
        response = requests.get(f"{BASE_URL}/news")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                news_count = len(data['data'])
                print(f"✅ 成功取得 {news_count} 筆最新消息")
                
                # 顯示分頁資訊
                if 'pagination' in data:
                    pagination = data['pagination']
                    print(f"   總數: {pagination['total']}")
                    print(f"   頁數: {pagination['pages']}")
                    print(f"   當前頁: {pagination['page']}")
                
                # 顯示前3筆消息
                for i, news in enumerate(data['data'][:3]):
                    print(f"   {i+1}. [{news['date']}] {news['title']}")
                
                return True
            else:
                print(f"❌ API回應錯誤: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 取得最新消息測試失敗: {e}")
        return False

def test_create_news():
    """測試建立最新消息"""
    print("\n=== 測試建立最新消息 ===")
    try:
        test_news = {
            'title': '測試消息 - API功能測試',
            'content': '這是一則測試消息，用來驗證API的建立功能是否正常運作。',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'link': 'test_news.html',
            'status': 'published'
        }
        
        response = requests.post(
            f"{BASE_URL}/news",
            json=test_news,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            if data['success']:
                print(f"✅ 成功建立測試消息: {data['data']['title']}")
                print(f"   ID: {data['data']['id']}")
                return data['data']['id']  # 返回新建立的消息ID
            else:
                print(f"❌ 建立消息失敗: {data.get('error', '未知錯誤')}")
                return None
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            print(f"回應內容: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 建立最新消息測試失敗: {e}")
        return None

def test_update_news(news_id):
    """測試更新最新消息"""
    if not news_id:
        print("\n=== 跳過更新測試（沒有可用的消息ID） ===")
        return False
    
    print(f"\n=== 測試更新最新消息 (ID: {news_id}) ===")
    try:
        update_data = {
            'title': '測試消息 - 已更新',
            'content': '這則測試消息已經被更新，用來驗證API的更新功能。'
        }
        
        response = requests.put(
            f"{BASE_URL}/news/{news_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 成功更新測試消息: {data['data']['title']}")
                return True
            else:
                print(f"❌ 更新消息失敗: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 更新最新消息測試失敗: {e}")
        return False

def test_update_news_status(news_id):
    """測試更新最新消息狀態"""
    if not news_id:
        print("\n=== 跳過狀態更新測試（沒有可用的消息ID） ===")
        return False
    
    print(f"\n=== 測試更新最新消息狀態 (ID: {news_id}) ===")
    try:
        # 先改為草稿狀態
        update_data = {'status': 'draft'}
        
        response = requests.patch(
            f"{BASE_URL}/news/{news_id}/status",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 成功更新狀態為: {data['data']['status']}")
                
                # 再改回已發布狀態
                update_data = {'status': 'published'}
                response = requests.patch(
                    f"{BASE_URL}/news/{news_id}/status",
                    json=update_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 成功更新狀態為: {data['data']['status']}")
                    return True
                else:
                    print(f"❌ 狀態更新失敗")
                    return False
            else:
                print(f"❌ 狀態更新失敗: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 狀態更新測試失敗: {e}")
        return False

def test_delete_news(news_id):
    """測試刪除最新消息"""
    if not news_id:
        print("\n=== 跳過刪除測試（沒有可用的消息ID） ===")
        return False
    
    print(f"\n=== 測試刪除最新消息 (ID: {news_id}) ===")
    try:
        response = requests.delete(f"{BASE_URL}/news/{news_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 成功刪除測試消息")
                return True
            else:
                print(f"❌ 刪除消息失敗: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 刪除最新消息測試失敗: {e}")
        return False

def test_news_search():
    """測試最新消息搜尋功能"""
    print("\n=== 測試最新消息搜尋功能 ===")
    try:
        # 測試搜尋功能
        response = requests.get(f"{BASE_URL}/news?search=測試")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 搜尋功能正常")
                print(f"   搜尋結果: {len(data['data'])} 筆")
            else:
                print(f"❌ 搜尋功能異常: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ 搜尋測試失敗: HTTP {response.status_code}")
            return False
        
        # 測試分頁功能
        response = requests.get(f"{BASE_URL}/news?page=1&limit=2")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 分頁功能正常")
                print(f"   每頁限制: {data['pagination']['per_page']}")
            else:
                print(f"❌ 分頁功能異常: {data.get('error', '未知錯誤')}")
                return False
        else:
            print(f"❌ 分頁測試失敗: HTTP {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 搜尋功能測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試GEIP最新消息API")
    print("=" * 50)
    
    # 測試連線
    if not test_api_connection():
        print("\n❌ API連線測試失敗，請先啟動後端服務")
        return
    
    # 測試健康檢查
    test_health_check()
    
    # 測試取得最新消息
    test_get_news()
    
    # 測試建立最新消息
    new_news_id = test_create_news()
    
    # 測試更新最新消息
    test_update_news(new_news_id)
    
    # 測試更新狀態
    test_update_news_status(new_news_id)
    
    # 測試搜尋功能
    test_news_search()
    
    # 測試刪除最新消息
    test_delete_news(new_news_id)
    
    print("\n" + "=" * 50)
    print("🎉 API測試完成！")
    
    # 最終檢查
    print("\n=== 最終檢查 ===")
    try:
        response = requests.get(f"{BASE_URL}/news")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                news_count = len(data['data'])
                print(f"目前資料庫中共有 {news_count} 筆最新消息")
            else:
                print("無法取得最新消息數量")
        else:
            print("無法連接到API進行最終檢查")
    except:
        print("最終檢查失敗")

if __name__ == '__main__':
    main()
