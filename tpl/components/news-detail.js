class NewsDetail extends HTMLElement{
  async connectedCallback(){
    this.src = this.getAttribute('src') || 'data/news.json';
    const res = await fetch(this.src);
    const items = await res.json();
    const params = new URLSearchParams(location.search);
    const id = parseInt(params.get('id')||'0',10);
    const found = items.find(i=>Number(i.id)===id) || items[0] || {};
    this.innerHTML = `
      <nav style="margin-bottom:12px"><a class="btn" href="news.html">← 返回公告列表</a></nav>
      <article class="card">
        <img class="news-card__thumb" src="${found.image||'assets/images/placeholder.jpg'}" alt="">
        <div class="card__body">
          <h1 style="margin-top:0">${found.title||'添加標題'}</h1>
          <p class="news-card__meta">${found.date||''}</p>
          <div style="white-space:pre-wrap;margin-top:12px">${(found.content||'添加摘要')}</div>
        </div>
      </article>
    `;
  }
}
customElements.define('news-detail', NewsDetail);