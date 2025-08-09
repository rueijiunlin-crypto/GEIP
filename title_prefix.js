// title_prefix.js
document.addEventListener("DOMContentLoaded", function() {
    const prefix = "綠色工程學系-"; // 這裡可以改成你要的前綴
    let currentTitle = document.title;

    // 如果標題沒有前綴才加
    if (!currentTitle.startsWith(prefix)) {
        document.title = prefix + currentTitle;
    }
    if (currentTitle !== prefix) {
        document.title = `${prefix} - ${currentTitle}`;
    }
});
// 這段程式碼會在頁面載入完成後執行，並檢查當前的標題是否已經有指定的前綴