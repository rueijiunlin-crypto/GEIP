# GEIP 後端系統

這是綠色工程產學共育實習學程的Python Flask後端系統，使用SQLite資料庫。

## 🏗️ 專案結構

```
backend/
├── app.py              # 主應用程式
├── config.py           # 設定檔
├── init_db.py          # 資料庫初始化腳本
├── test_api.py         # API測試腳本
├── requirements.txt    # 依賴套件
├── README.md           # 說明文件
├── models/             # 資料模型
│   ├── __init__.py
│   └── news.py         # 最新消息模型
├── routes/             # 路由控制
│   ├── __init__.py
│   └── news.py         # 最新消息API
└── utils/              # 工具函數
    ├── __init__.py
    └── database.py     # 資料庫操作
```

## 🚀 快速開始

### 1. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2. 初始化資料庫
```bash
python init_db.py
```

### 3. 啟動後端服務
```bash
python app.py
```

服務將在 `http://localhost:5000` 啟動

## 📚 API端點

### 測試端點
- `GET /api/test` - 測試API連線
- `GET /api/health` - 健康檢查

### 最新消息管理
- `GET /api/news` - 取得所有最新消息
  - 查詢參數：
    - `page`: 頁碼（預設1）
    - `limit`: 每頁數量（預設10）
    - `status`: 狀態篩選（published/draft/archived）
    - `search`: 關鍵字搜尋
    - `date_from`: 開始日期（YYYY-MM-DD）
    - `date_to`: 結束日期（YYYY-MM-DD）

- `GET /api/news/<id>` - 取得特定最新消息
- `POST /api/news` - 建立新最新消息
- `PUT /api/news/<id>` - 更新最新消息
- `DELETE /api/news/<id>` - 刪除最新消息
- `PATCH /api/news/<id>/status` - 更新最新消息狀態

## 🧪 測試

### 執行測試腳本
```bash
python test_api.py
```

測試腳本會驗證：
- ✅ API連線測試
- ✅ 健康檢查
- ✅ 取得最新消息
- ✅ 建立新消息
- ✅ 更新消息
- ✅ 更新狀態
- ✅ 搜尋功能
- ✅ 刪除消息

## 📊 資料庫結構

### News 資料表
- `id` - 主鍵
- `title` - 標題（必填，最大200字元）
- `content` - 內容（最大5000字元）
- `date` - 日期（必填，YYYY-MM-DD格式）
- `link` - 連結（可選）
- `status` - 狀態（published/draft/archived）
- `created_at` - 建立時間
- `updated_at` - 更新時間

## ⚙️ 設定

### 環境變數
- `FLASK_ENV`: 環境設定（development/production/testing）
- `SECRET_KEY`: 應用程式密鑰
- `DATABASE_URL`: 資料庫連線字串

### 設定檔
- `config.py`: 包含開發、生產、測試環境的設定
- 可調整每頁顯示數量、字元長度限制等

## 🔧 開發

### 新增功能模組
1. 在 `models/` 建立資料模型
2. 在 `routes/` 建立API路由
3. 在 `app.py` 註冊新路由

### 資料庫操作
- 使用 `utils/database.py` 中的工具函數
- 支援分頁、日期格式化、字串清理等

## 📝 注意事項

1. 確保Python 3.7+版本
2. 首次運行需要執行 `init_db.py` 初始化資料庫
3. 後端服務預設在5000端口，請確保該端口未被占用
4. 開發環境會自動建立資料表
5. 支援從現有JSON檔案匯入資料

## 🐛 故障排除

### 常見問題
1. **端口被占用**: 修改 `app.py` 中的端口號
2. **資料庫錯誤**: 檢查 `geip.db` 檔案權限
3. **匯入失敗**: 確認 `assets/data/news.json` 路徑正確

### 日誌
- 應用程式會輸出詳細的日誌資訊
- 包含資料庫操作、API請求等記錄

## 📞 支援

如有問題，請檢查：
1. 日誌輸出
2. 資料庫連線狀態
3. API回應格式
4. 網路連線設定
