// title_prefix.js
document.addEventListener("DOMContentLoaded", () => {
  const PREFIX = "綠色工程產學共育實習學程";

  // 先拿 <title>
  let pageName = (document.title || "").trim();

  // 某些模板會留 "(title)"，視同沒填
  if (!pageName || pageName === "(title)") {
    // 退而求其次：用頁面的 <h1>
    const h1 = document.querySelector("h1");
    if (h1) pageName = h1.textContent.trim();
  }

  // 再不行就用檔名對照
  if (!pageName) {
    const file = (location.pathname.split("/").pop() || "index.html")
      .replace(/\.html?$/i, "");
    const map = {
      index: "首頁",
      origin: "計畫緣起",
      goal: "計畫目標",
      faculty: "師資介紹",
      news: "最新消息",
      rules: "修課規範",
      curriculum: "課程規劃表",
      apply: "申請流程與表單",
      certificate: "學程證書說明",
      cross_discipline: "跨領域實務專題",
      partners: "合作企業",
      project_showcase: "專題成果展示",
      internship_rules: "實習修課規定",
      internship_partners: "實習合作企業",
      intern_experience: "實習經驗分享",
      videos: "特色單元影片",
      materials: "課程教材下載區",
      contact: "聯絡我們",
      faq: "常見問答",
      links: "相關網站",
      gallery: "活動花絮",
    };
    pageName = map[file] || file;
  }

  document.title = `${PREFIX} - ${pageName}`;
});
