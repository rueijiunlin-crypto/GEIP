class BannerCarousel extends HTMLElement{
  constructor(){ super(); this.index = 0; this.timer = null; }
  connectedCallback(){
    const slides = JSON.parse(this.getAttribute('slides')||'[]');
    this.slides = slides.length?slides:[
      {text:'添加圖片', bg:'#94a3b8'},
      {text:'添加圖片', bg:'#64748b'},
      {text:'添加圖片', bg:'#475569'}
    ];
    this.render();
    this.start();
    this.addEventListener('mouseenter',()=>this.stop());
    this.addEventListener('mouseleave',()=>this.start());
  }
  render(){
    this.innerHTML = `
      <div class="carousel card">
        <div class="carousel__slides" style="transform: translateX(-${this.index*100}%);">
          ${this.slides.map(s=>`<div class="carousel__slide" style="background:${s.bg||'#94a3b8'}">${s.text||'添加圖片'}</div>`).join('')}
        </div>
        <div class="carousel__dots">
          ${this.slides.map((_,i)=>`<button class="carousel__dot ${i===this.index?'is-active':''}" aria-label="切換到第 ${i+1} 張" data-i="${i}"></button>`).join('')}
        </div>
      </div>
    `;
    this.querySelectorAll('.carousel__dot').forEach(btn=>{
      btn.addEventListener('click',()=>{ this.index = Number(btn.dataset.i); this.render(); });
    });
  }
  start(){ if(this.timer) return; this.timer=setInterval(()=>{ this.index=(this.index+1)%this.slides.length; this.render(); }, 4000); }
  stop(){ clearInterval(this.timer); this.timer=null; }
}
customElements.define('banner-carousel', BannerCarousel);