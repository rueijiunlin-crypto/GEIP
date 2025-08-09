function ytIdFromUrl(url){
  if(!url) return null;
  try{
    const u = new URL(url);
    if(u.hostname.includes('youtu.be')){
      return u.pathname.slice(1);
    }
    if(u.searchParams.get('v')) return u.searchParams.get('v');
    const paths = u.pathname.split('/').filter(Boolean);
    const watch = paths[0];
    return null;
  }catch(e){
    return null;
  }
}
class VideoEmbed extends HTMLElement{
  connectedCallback(){
    const url = this.getAttribute('url')||'';
    const vid = this.getAttribute('video-id') || ytIdFromUrl(url);
    const title = this.getAttribute('title') || '添加標題';
    const ratio = this.getAttribute('ratio') || '16/9';
    if(!vid){
      this.innerHTML = `<div class="card"><div class="card__body"><p>YOUTUBE：添加YOUTUBE連結</p></div></div>`;
      return;
    }
    this.innerHTML = `
      <div class="card">
        <div class="card__body">
          <div style="position:relative;width:100%;aspect-ratio:${ratio};">
            <iframe width="100%" height="100%" src="https://www.youtube.com/embed/${vid}" 
              title="${title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen loading="lazy"></iframe>
          </div>
          <h3 style="margin-top:12px">${title}</h3>
        </div>
      </div>
    `;
  }
}
customElements.define('video-embed', VideoEmbed);