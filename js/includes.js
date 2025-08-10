document.addEventListener('DOMContentLoaded', async () => {
  const nodes = document.querySelectorAll('[data-include]');
  for (const el of nodes) {
    const url = el.getAttribute('data-include');
    try {
      const res = await fetch(url + (url.includes('?') ? '&' : '?') + 'v=' + Date.now());
      const html = await res.text();
      el.outerHTML = html;
    } catch (e) {
      console.error('載入 include 失敗：', url, e);
    }
  }
});