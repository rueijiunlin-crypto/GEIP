class NewsList extends HTMLElement{
  async connectedCallback(){
    const src = this.getAttribute('src') || 'data/news.json';
    const res = await fetch(src);
    const items = await res.json();
    const top = items.slice(0,6);
    this.innerHTML = `
      <div class="grid cols-3">
        ${top.map(n=>`
          <article class="card">
            <img class="news-card__thumb" src="${n.image||'assets/images/placeholder.jpg'}" alt="">
            <div class="card__body">
              <h3 style="margin:0 0 8px 0">${n.title||'添加標題'}</h3>
              <p class="news-card__meta">${n.date||'2025-08-08'}</p>
              <p>${n.summary||'添加摘要'}</p>
              <a class="btn" href="news-detail.html">閱讀更多</a>
            </div>
          </article>
        `).join('')}
      </div>
    `;
  }
}
customElements.define('news-list', NewsList);