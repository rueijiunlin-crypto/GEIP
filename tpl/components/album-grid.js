class AlbumGrid extends HTMLElement{
  async connectedCallback(){
    const src = this.getAttribute('src') || 'data/albums.json';
    const res = await fetch(src);
    const items = await res.json();
    const top = items.slice(0,9);
    this.innerHTML = `
      <div class="grid cols-3">
        ${top.map(a=>`
          <figure class="card" style="overflow:hidden">
            <img src="${a.cover||'assets/images/placeholder.jpg'}" alt="" style="width:100%;aspect-ratio:4/3;object-fit:cover">
            <figcaption class="card__body">
              <div style="font-weight:700">${a.title||'添加標題'}</div>
              <div style="color:#6b7280;font-size:.9rem;margin-top:4px">${a.date||'2025-08-08'}</div>
            </figcaption>
          </figure>
        `).join('')}
      </div>
    `;
  }
}
customElements.define('album-grid', AlbumGrid);