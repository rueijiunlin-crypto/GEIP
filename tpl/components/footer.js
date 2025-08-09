class SiteFooter extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `
      <footer class="footer">
        <div class="container footer__inner">
          <div>
            <div style="font-weight:800; font-size:1.1rem;">GEIP</div>
            <div style="margin-top:6px;">綠色工程產學共育實習學程</div>
            <div style="margin-top:6px; font-size:0.9rem;">© 2025 All rights reserved.</div>
          </div>
          <div>
            <div style="font-weight:700; margin-bottom:8px;">快速連結</div>
            <div style="display:flex; flex-direction:column; gap:6px;">
              <a href="news.html">訊息公告</a>
              <a href="projects.html">專題成果</a>
              <a href="resources-videos.html">特色單元影片</a>
              <a href="contact.html">聯絡我們</a>
            </div>
          </div>
        </div>
      </footer>
    `;
  }
}
customElements.define('site-footer', SiteFooter);