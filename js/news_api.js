// js/news_api.js - 最新消息API整合
(function () {
  'use strict';

  // API配置 - 直接指定後端API端口
  const API_BASE_URL = 'http://127.0.0.1:5000/api';
  const NEWS_API_URL = `${API_BASE_URL}/news`;
  
  // 快取設定
  const CACHE_KEY = 'geip_news_cache';
  const CACHE_DURATION = 5 * 60 * 1000; // 5分鐘快取

  // 最新消息容器選擇器
  const NEWS_CONTAINERS = {
    'index': '#latestNewsContainer',           // 首頁最新消息
    'news': '#newsListContainer',              // 最新消息頁面
    'sidebar': '#sidebarNewsContainer'         // 側邊欄最新消息
  };

  // 取得快取的最新消息
  function getCachedNews() {
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (cached) {
        const data = JSON.parse(cached);
        if (Date.now() - data.timestamp < CACHE_DURATION) {
          return data.news;
        }
      }
    } catch (error) {
      console.warn('讀取快取失敗:', error);
    }
    return null;
  }

  // 儲存最新消息到快取
  function cacheNews(news) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        news: news,
        timestamp: Date.now()
      }));
    } catch (error) {
      console.warn('儲存快取失敗:', error);
    }
  }

  // 從API取得最新消息
  async function fetchNewsFromAPI() {
    try {
      console.log('發送API請求到:', NEWS_API_URL);
      
      const response = await fetch(NEWS_API_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });

      console.log('API回應狀態:', response.status, response.statusText);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

             const data = await response.json();
       console.log('API原始回應:', data);
       
       if (data.success) {
         console.log('API資料陣列:', data.data);
         console.log('第一筆資料結構:', data.data[0]);
         
         // 暫時顯示所有消息進行測試
         const allNews = data.data.sort((a, b) => new Date(b.date) - new Date(a.date));
         console.log('排序後的所有消息:', allNews);
         
         // 只返回已發布的消息，按日期排序
         const publishedNews = data.data
           .filter(item => {
             console.log('檢查項目:', item, '狀態:', item.status, '類型:', typeof item.status);
             return item.status === 'published';
           })
           .sort((a, b) => new Date(b.date) - new Date(a.date));
         
         console.log('過濾後的已發布消息:', publishedNews);
         
         // 如果過濾後沒有消息，暫時返回所有消息
         if (publishedNews.length === 0) {
           console.log('過濾後沒有已發布消息，暫時顯示所有消息');
           return allNews;
         }
         
         return publishedNews;
      } else {
        throw new Error(data.message || '取得最新消息失敗');
      }
    } catch (error) {
      console.error('API請求失敗:', error);
      throw error;
    }
  }

  // 格式化日期
  function formatDate(dateString) {
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 1) {
        return '今天';
      } else if (diffDays === 2) {
        return '昨天';
      } else if (diffDays <= 7) {
        return `${diffDays - 1}天前`;
      } else {
        return date.toLocaleDateString('zh-TW', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
    } catch (error) {
      return dateString;
    }
  }

  // 截斷文字
  function truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + '...';
  }

  // 渲染首頁最新消息
  function renderIndexNews(news) {
    const container = document.querySelector(NEWS_CONTAINERS.index);
    console.log('渲染首頁最新消息，容器:', container, '新聞數量:', news.length);
    
    if (!container) {
      console.warn('找不到首頁最新消息容器:', NEWS_CONTAINERS.index);
      return;
    }
    
    if (!news.length) {
      container.innerHTML = `
        <div class="col-12 text-center">
          <p class="text-muted">目前沒有最新消息</p>
        </div>
      `;
      return;
    }

    const latestNews = news.slice(0, 3); // 只顯示最新3則
    console.log('渲染首頁最新消息:', latestNews);
    
    const html = latestNews.map(item => `
      <div class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">
              <a href="${item.link || '#'}" class="text-decoration-none">
                ${escapeHtml(item.title)}
              </a>
            </h5>
            <p class="card-text text-muted">
              ${escapeHtml(truncateText(item.content, 80))}
            </p>
            <div class="d-flex justify-content-between align-items-center">
              <small class="text-muted">
                <i class="bi bi-calendar3"></i>
                ${formatDate(item.date)}
              </small>
              ${item.link ? `
                <a href="${item.link}" class="btn btn-sm btn-outline-primary">
                  閱讀更多
                </a>
              ` : ''}
            </div>
          </div>
        </div>
      </div>
    `).join('');

    container.innerHTML = html;
    console.log('首頁最新消息渲染完成');
  }

  // 渲染最新消息頁面
  function renderNewsPage(news) {
    const container = document.querySelector(NEWS_CONTAINERS.news);
    if (!container || !news.length) return;

    const html = news.map(item => `
      <div class="col-lg-6 col-md-12 mb-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">
              <a href="${item.link || '#'}" class="text-decoration-none">
                ${escapeHtml(item.title)}
              </a>
            </h5>
            <p class="card-text">
              ${escapeHtml(truncateText(item.content, 150))}
            </p>
            <div class="d-flex justify-content-between align-items-center">
              <small class="text-muted">
                <i class="bi bi-calendar3"></i>
                ${formatDate(item.date)}
              </small>
              ${item.link ? `
                <a href="${item.link}" class="btn btn-outline-primary">
                  閱讀更多
                </a>
              ` : ''}
            </div>
          </div>
        </div>
      </div>
    `).join('');

    container.innerHTML = html;
  }

  // 渲染側邊欄最新消息
  function renderSidebarNews(news) {
    const container = document.querySelector(NEWS_CONTAINERS.sidebar);
    if (!container || !news.length) return;

    const sidebarNews = news.slice(0, 5); // 側邊欄顯示5則
    
    const html = `
      <div class="list-group list-group-flush">
        ${sidebarNews.map(item => `
          <a href="${item.link || '#'}" class="list-group-item list-group-item-action border-0 px-0">
            <div class="d-flex w-100 justify-content-between">
              <h6 class="mb-1">${escapeHtml(truncateText(item.title, 40))}</h6>
              <small class="text-muted">${formatDate(item.date)}</small>
            </div>
            <p class="mb-1 small text-muted">
              ${escapeHtml(truncateText(item.content, 60))}
            </p>
          </a>
        `).join('')}
      </div>
    `;

    container.innerHTML = html;
  }

  // 渲染所有容器
  function renderAllNews(news) {
    renderIndexNews(news);
    renderNewsPage(news);
    renderSidebarNews(news);
  }

  // 顯示錯誤訊息
  function showError(message) {
    console.error('最新消息載入失敗:', message);
    
    // 在所有容器顯示錯誤訊息
    Object.values(NEWS_CONTAINERS).forEach(selector => {
      const container = document.querySelector(selector);
      if (container) {
        container.innerHTML = `
          <div class="alert alert-warning" role="alert">
            <i class="bi bi-exclamation-triangle"></i>
            最新消息載入失敗，請稍後再試
          </div>
        `;
      }
    });
  }

  // 顯示載入中狀態
  function showLoading() {
    Object.values(NEWS_CONTAINERS).forEach(selector => {
      const container = document.querySelector(selector);
      if (container) {
        container.innerHTML = `
          <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">載入中...</span>
            </div>
            <p class="mt-2 text-muted">載入最新消息中...</p>
          </div>
        `;
      }
    });
  }

  // 主要載入函數
  async function loadNews() {
    try {
      console.log('開始載入最新消息...');
      
      // 先檢查快取
      let news = getCachedNews();
      
      if (!news) {
        console.log('快取無效，從API載入...');
        // 顯示載入中
        showLoading();
        
        // 從API取得資料
        news = await fetchNewsFromAPI();
        console.log('API回應:', news);
        
        // 儲存到快取
        cacheNews(news);
      } else {
        console.log('使用快取資料:', news);
      }

      // 渲染最新消息
      renderAllNews(news);
      console.log('最新消息渲染完成');
      
    } catch (error) {
      console.error('載入最新消息時發生錯誤:', error);
      showError(error.message);
    }
  }

  // HTML轉義函數
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 手動重新載入最新消息
  function refreshNews() {
    // 清除快取
    localStorage.removeItem(CACHE_KEY);
    // 重新載入
    loadNews();
  }

  // 綁定重新載入按鈕
  function bindRefreshButton() {
    const refreshBtn = document.querySelector('#refreshNewsBtn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', refreshNews);
    }
  }

  // 初始化
  function init() {
    console.log('初始化最新消息API整合...');
    
    // 檢查是否有最新消息容器
    const hasNewsContainer = Object.values(NEWS_CONTAINERS).some(selector => {
      const container = document.querySelector(selector);
      console.log('檢查容器:', selector, container);
      return container;
    });

    console.log('是否有最新消息容器:', hasNewsContainer);

    if (hasNewsContainer) {
      console.log('開始載入最新消息...');
      loadNews();
      bindRefreshButton();
    } else {
      console.warn('沒有找到最新消息容器，跳過初始化');
    }
  }

  // 頁面載入完成後初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露給全域使用
  window.GEIPNews = {
    loadNews,
    refreshNews,
    fetchNewsFromAPI
  };

})();
