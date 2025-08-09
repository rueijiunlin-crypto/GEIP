class VideosList extends HTMLElement{
  async connectedCallback(){
    const src = this.getAttribute('src') || 'data/videos.json';
    const res = await fetch(src);
    const items = await res.json();
    const pageSize = Number(this.getAttribute('page-size')||6);
    const params = new URLSearchParams(location.search);
    const page = Math.max(1, parseInt(params.get('page')||'1',10));
    const start = (page-1)*pageSize;
    const pageItems = items.slice(start, start+pageSize);
    const total = Math.ceil(items.length/pageSize);
    this.innerHTML = `
      <div class="grid cols-3">
        ${pageItems.map(v=>`<video-embed url="${v.url||''}" title="${v.title||'添加標題'}"></video-embed>`).join('')}
      </div>
      <nav aria-label="分頁導覽" style="display:flex;gap:6px;justify-content:center;margin-top:16px;flex-wrap:wrap">
        ${Array.from({length: total}, (_,i)=>i+1).map(i=>`
          <button class="btn" data-page="${i}" ${i===page?'disabled':''}>${i}</button>
        `).join('')}
      </nav>
    `;
    this.querySelectorAll('button[data-page]').forEach(b=>{
      b.addEventListener('click', ()=>{
        const url = new URL(location.href);
        url.searchParams.set('page', b.dataset.page);
        location.href = url.toString();
      });
    });
  }
}
customElements.define('videos-list', VideosList);