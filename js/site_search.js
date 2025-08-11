// js/site_search.js
(function () {
  const PAGES_URL = 'search_pages.json';          // 要抓取的頁面清單
  const CACHE_KEY = 'siteSearchIndexV1';          // localStorage key
  const MAX_AGE = 1000 * 60 * 60 * 24;            // 緩存一天
  let indexData = null;

  // 取得/建立索引
  async function getIndex() {
    // 先讀緩存
    try {
      const cached = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null');
      if (cached && (Date.now() - cached.time < MAX_AGE) && Array.isArray(cached.data)) {
        return cached.data;
      }
    } catch (_) {}

    // 重新建立
    const pages = await (await fetch(PAGES_URL, { cache: 'no-store' })).json();
    const out = [];
    for (const url of pages) {
      try {
        const res = await fetch(url, { cache: 'no-store' });
        const html = await res.text();

        const doc = new DOMParser().parseFromString(html, 'text/html');

        // 取得 title
        const title = (doc.querySelector('title')?.textContent ||
                      doc.querySelector('h1')?.textContent ||
                      url).trim();

        // 選正文 root：優先 main，其次 .container，再不行就 body
        let root = doc.querySelector('main') || doc.querySelector('.container') || doc.body;

        // 移除非正文元素
        root.querySelectorAll('nav, footer, script, style').forEach(n => n.remove());

        // 抽出文字
        const text = root.textContent.replace(/\s+/g, ' ').trim();

        out.push({ url, title, text });
      } catch (err) {
        console.warn('[search] 讀取頁面失敗：', url, err);
      }
    }

    // 存緩存
    localStorage.setItem(CACHE_KEY, JSON.stringify({ time: Date.now(), data: out }));
    return out;
  }

  // 關鍵字比對 + 片段
  function doSearch(q, data) {
    const lc = q.toLowerCase();
    const results = [];
    for (const it of data) {
      const pos = it.text.toLowerCase().indexOf(lc);
      if (pos !== -1) {
        const start = Math.max(0, pos - 50);
        const end   = Math.min(it.text.length, pos + q.length + 100);
        let snippet = it.text.slice(start, end).trim();

        // 高亮
        const re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        snippet = snippet.replace(re, m => `<mark>${m}</mark>`);

        results.push({ url: it.url, title: it.title, snippet });
      }
    }
    // 可以再加排序（出現次數等），當前簡單依找到順序
    return results;
  }

  // 顯示結果到 Modal
  function renderResults(q, results) {
    const modalEl  = document.getElementById('searchResultsModal');
    const modalBody = document.getElementById('searchResultsBody');
    if (!modalEl || !modalBody) return;

    let html = '';
    if (!results.length) {
      html = `<p class="text-muted mb-0">找不到與「<strong>${escapeHtml(q)}</strong>」相關的內容。</p>`;
    } else {
      html = `<p class="text-muted">共 ${results.length} 筆結果：</p>
              <div class="list-group">` +
              results.map(r => `
                <a class="list-group-item list-group-item-action" href="${r.url}">
                  <div class="fw-bold">${escapeHtml(r.title)}</div>
                  <div class="small text-muted search-hit">${r.snippet}…</div>
                </a>
              `).join('') +
             `</div>`;
    }
    modalBody.innerHTML = html;

    // 開 modal
    const m = new bootstrap.Modal(modalEl);
    m.show();
  }

  // 搜尋流程
  async function handleSearch(qRaw) {
    const q = (qRaw || '').trim();
    if (!q) return;
    try {
      indexData = indexData || await getIndex();
      const results = doSearch(q, indexData);
      renderResults(q, results);
    } catch (err) {
      console.error('[search] 發生錯誤：', err);
    }
  }

  // 綁定兩個表單（桌機 + 手機）
  function bindForms() {
    const formDesktop = document.getElementById('siteSearchForm');
    const inputDesktop = document.getElementById('siteSearchInput');
    const formMobile  = document.getElementById('siteSearchFormMobile');
    const inputMobile = document.getElementById('siteSearchInputMobile');

    formDesktop && formDesktop.addEventListener('submit', e => {
      e.preventDefault();
      handleSearch(inputDesktop.value);
    });

    formMobile && formMobile.addEventListener('submit', e => {
      e.preventDefault();
      handleSearch(inputMobile.value);
    });
  }

  // 小工具：HTML escape
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[c]));
  }

  // 初始化
  document.addEventListener('DOMContentLoaded', bindForms);
})();
