// title_prefix.js  (v2)
document.addEventListener("DOMContentLoaded", () => {
  const PREFIX = "綠色工程產學共育實習學程";

  // 取得目前 <title>
  let t = (document.title || "").trim();

  // 某些模板會留 "(title)"，視同沒填
  if (!t || t === "(title)") {
    const h1 = document.querySelector("h1");
    if (h1) t = h1.textContent.trim();
  }

  // 若仍然沒有，退而求其次用檔名對照表
  if (!t) {
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
    t = map[file] || file;
  }

  // ✅ 先把舊前綴或多餘連字號拿掉（例如「綠色工程學系 - 首頁」或「任何字 - 首頁」）
  t = t.replace(
    /^(綠色工程學系|綠色工程產學共育實習學程)\s*[-–—]\s*/i,
    ""
  ).replace(/^\s*[-–—]\s*/, ""); // 防止原本就有開頭的 -

  // 最終套用新前綴
  document.title = `${PREFIX} - ${t}`;
});
