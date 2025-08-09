class CourseTable extends HTMLElement{
  async connectedCallback(){
    const src = this.getAttribute('src') || 'data/courses.json';
    const res = await fetch(src);
    const rows = await res.json();
    const header = ['年度','學期','課名','學分','類別','教師'];
    this.innerHTML = `
      <div class="card">
        <div class="card__body" style="overflow:auto">
          <table style="width:100%;border-collapse:collapse;min-width:720px">
            <thead>
              <tr>
                ${header.map(h=>`<th style="text-align:left;padding:10px;border-bottom:1px solid #e5e7eb">${h}</th>`).join('')}
              </tr>
            </thead>
            <tbody>
              ${rows.map(r=>`
                <tr>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.year||''}</td>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.semester||''}</td>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.name||'添加標題'}</td>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.credits||''}</td>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.type||''}</td>
                  <td style="padding:10px;border-bottom:1px solid #f1f5f9">${r.teacher||''}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
}
customElements.define('course-table', CourseTable);