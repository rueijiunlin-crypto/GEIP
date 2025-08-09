class AppNavbar extends HTMLElement{
  connectedCallback(){
    const links = JSON.parse(this.getAttribute('links')||'[]');
    const brand = this.getAttribute('brand') || 'GEIP';
    this.innerHTML = `
      <nav class="navbar">
        <div class="container navbar__inner">
          <a class="navbar__brand" href="index.html">${brand}</a>
          <div class="navbar__menu" role="navigation" aria-label="主選單">
            ${links.map(l=>`<a class="navbar__link" href="${l.href}">${l.text}</a>`).join('')}
          </div>
        </div>
      </nav>
      <div class="header-spacer" aria-hidden="true"></div>
    `;
  }
}
customElements.define('app-navbar', AppNavbar);