class NewsPaginated extends HTMLElement{
  async connectedCallback(){
    this.src = this.getAttribute('src') || 'data/news.json';
    this.pageSize = Number(this.getAttribute('page-size')||6);
    await this.load();
    this.render();
  }
  async load(){
    const res = await fetch(this.src);
    this.items = await res.json();
    // sort by date desc if possible
    this.items.sort((a,b)=> (b.date||'').localeCompare(a.date||''));
    const params = new URLSearchParams(location.search);
    this.page = Math.max(1, parseInt(params.get('page')||'1',10));
  }
  go(p){
    const total = Math.ceil(this.items.length/this.pageSize);
    const next = Math.min(Math.max(1,p), total);
    const url = new URL(location.href);
    url.searchParams.set('page', String(next));
    history.pushState({}, '', url);
    this.page = next;
    this.render();
  }
  render(){
    const start = (this.page-1)*this.pageSize;
    const pageItems = this.items.slice(start, start+this.pageSize);
    const total = Math.ceil(this.items.length/this.pageSize);
    this.innerHTML = `
      <div class="grid cols-3">
        ${pageItems.map(n=>`
          <article class="card">
            <img class="news-card__thumb" src="${n.image||'assets/images/placeholder.jpg'}" alt="">
            <div class="card__body">
              <h3 style="margin:0 0 8px 0">${n.title||'添加標題'}</h3>
              <p class="news-card__meta">${n.date||''}</p>
              <p>${n.summary||'添加摘要'}</p>
              <a class="btn" href="news-detail.html?id=${n.id}">閱讀更多</a>
            </div>
          </article>
        `).join('')}
      </div>
      <nav aria-label="分頁導覽" style="display:flex;gap:6px;justify-content:center;margin-top:16px;flex-wrap:wrap">
        <button class="btn" data-page="first" ${this.page===1?'disabled':''}>第一頁</button>
        <button class="btn" data-page="prev" ${this.page===1?'disabled':''}>上一頁</button>
        ${Array.from({length: total}, (_,i)=>i+1).map(i=>`
          <button class="btn" data-page="${i}" ${i===this.page?'disabled':''}>${i}</button>
        `).join('')}
        <button class="btn" data-page="next" ${this.page===total?'disabled':''}>下一頁</button>
        <button class="btn" data-page="last" ${this.page===total?'disabled':''}>最後一頁</button>
      </nav>
    `;
    this.querySelectorAll('button[data-page]').forEach(b=>{
      b.addEventListener('click', ()=>{
        const t = b.dataset.page;
        const total = Math.ceil(this.items.length/this.pageSize);
        if(t==='first') return this.go(1);
        if(t==='prev') return this.go(this.page-1);
        if(t==='next') return this.go(this.page+1);
        if(t==='last') return this.go(total);
        return this.go(Number(t));
      });
    });
  }
}
customElements.define('news-paginated', NewsPaginated);