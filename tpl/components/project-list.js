
class ProjectList extends HTMLElement{
  async connectedCallback(){
    this.src = this.getAttribute('src') || 'data/projects.json';
    this.pageSize = Number(this.getAttribute('page-size')||9);
    await this.load();
    this.render();
  }
  async load(){
    const res = await fetch(this.src);
    this.all = await res.json();
    this.currentYear = '全部';
    const params = new URLSearchParams(location.search);
    this.page = Math.max(1, parseInt(params.get('page')||'1',10));
  }
  filterByYear(items){
    return this.currentYear==='全部' ? items : items.filter(p=>String(p.year)===String(this.currentYear));
  }
  go(p){
    const total = Math.ceil(this.filterByYear(this.all).length/this.pageSize);
    const next = Math.min(Math.max(1,p), total);
    const url = new URL(location.href);
    url.searchParams.set('page', String(next));
    history.pushState({}, '', url);
    this.page = next;
    this.render();
  }
  render(){
    const years = Array.from(new Set(this.all.map(p=>p.year))).sort((a,b)=>b-a);
    const filtered = this.filterByYear(this.all);
    const total = Math.ceil(filtered.length/this.pageSize);
    const start = (this.page-1)*this.pageSize;
    const show = filtered.slice(start, start+this.pageSize);
    this.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap">
        <span style="font-weight:700">年度：</span>
        <button class="btn" data-year="全部" ${this.currentYear==='全部'?'disabled':''}>全部</button>
        ${years.map(y=>`<button class="btn" data-year="${y}" ${String(y)===String(this.currentYear)?'disabled':''}>${y}</button>`).join('')}
      </div>
      <div class="grid cols-3">
        ${show.map(p=>`
          <article class="card">
            <img src="${p.thumb||'assets/images/placeholder.jpg'}" alt="" style="width:100%;aspect-ratio:16/9;object-fit:cover">
            <div class="card__body">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <h3 style="margin:0">${p.title||'添加標題'}</h3>
                <span style="font-size:.85rem;background:#e5f3f1;color:#065f46;padding:2px 8px;border-radius:999px">${p.year||'2025'}</span>
              </div>
              <p style="color:#6b7280;font-size:.95rem;margin:.5rem 0">${p.abstract||'添加摘要'}</p>
              <div style="font-size:.9rem;color:#334155">指導：${(p.advisors||['—']).join('、')}</div>
              <div style="font-size:.9rem;color:#334155">成員：${(p.members||['—']).join('、')}</div>
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
    this.querySelectorAll('button[data-year]').forEach(b=>{
      b.addEventListener('click', ()=>{
        this.currentYear = b.dataset.year;
        this.page = 1;
        this.render();
      });
    });
    this.querySelectorAll('button[data-page]').forEach(b=>{
      b.addEventListener('click', ()=>{
        const t = b.dataset.page;
        const totalPages = Math.ceil(this.filterByYear(this.all).length/this.pageSize);
        if(t==='first') return this.go(1);
        if(t==='prev') return this.go(this.page-1);
        if(t==='next') return this.go(this.page+1);
        if(t==='last') return this.go(totalPages);
        return this.go(Number(t));
      });
    });
  }
}
customElements.define('project-list', ProjectList);

// Enhance with simple pagination by page-size attribute
ProjectList.prototype.render = (function(orig){
  return function(show, all){
    const pageSize = Number(this.getAttribute('page-size')||9);
    const params = new URLSearchParams(location.search);
    const page = Math.max(1, parseInt(params.get('page')||'1',10));
    const start = (page-1)*pageSize;
    const pageItems = show.slice(start, start+pageSize);
    const total = Math.ceil(show.length/pageSize);
    const years = Array.from(new Set(all.map(p=>p.year))).sort((a,b)=>b-a);
    this.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap">
        <span style="font-weight:700">年度：</span>
        <button class="btn" data-year="全部">全部</button>
        ${years.map(y=>`<button class="btn" data-year="${y}">${y}</button>`).join('')}
      </div>
      <div class="grid cols-3">
        ${pageItems.map(p=>`
          <article class="card">
            <img src="${p.thumb||'assets/images/placeholder.jpg'}" alt="" style="width:100%;aspect-ratio:16/9;object-fit:cover">
            <div class="card__body">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <h3 style="margin:0">${p.title||'添加標題'}</h3>
                <span style="font-size:.85rem;background:#e5f3f1;color:#065f46;padding:2px 8px;border-radius:999px">${p.year||'2025'}</span>
              </div>
              <p style="color:#6b7280;font-size:.95rem;margin:.5rem 0">${p.abstract||'添加摘要'}</p>
              <div style="font-size:.9rem;color:#334155">指導：${(p.advisors||['—']).join('、')}</div>
              <div style="font-size:.9rem;color:#334155">成員：${(p.members||['—']).join('、')}</div>
            </div>
          </article>
        `).join('')}
      </div>
      <nav aria-label="分頁導覽" style="display:flex;gap:6px;justify-content:center;margin-top:16px;flex-wrap:wrap">
        ${Array.from({length: total}, (_,i)=>i+1).map(i=>`
          <button class="btn" data-page="${i}" ${i===page?'disabled':''}>${i}</button>
        `).join('')}
      </nav>
    `;
    this.querySelectorAll('button[data-year]').forEach(b=>{
      b.addEventListener('click', async ()=>{
        const y = b.dataset.year;
        const res = await fetch(this.getAttribute('src') || 'data/projects.json');
        const items = await res.json();
        const next = y==='全部'? items : items.filter(p=>String(p.year)===String(y));
        // Reset to first page when changing year
        const url = new URL(location.href);
        url.searchParams.delete('page');
        history.replaceState({}, '', url);
        this.render(next.slice(0, Math.max(pageSize, next.length)), items);
      });
    });
    this.querySelectorAll('button[data-page]').forEach(b=>{
      b.addEventListener('click', ()=>{
        const url = new URL(location.href);
        url.searchParams.set('page', b.dataset.page);
        location.href = url.toString();
      });
    });
  }
})(ProjectList.prototype.render);
