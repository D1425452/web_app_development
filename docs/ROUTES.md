# 路由與頁面設計 (Routes Design)

本文件依據 PRD 與資料庫架構，設計系統中所有的 URL 路徑、HTTP 請求方法與其對應的頁面與處理邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :---: | :--- | :--- | :--- |
| **首頁 (所有食譜)** | GET | `/` | `templates/index.html` | 顯示所有食譜列表 |
| **搜尋食譜** | GET | `/search` | `templates/index.html` | 接收 `?q=xxx` 並顯示搜尋結果 |
| **我的最愛列表** | GET | `/favorites` | `templates/index.html` | 顯示所有被標記為最愛的食譜 |
| **特定標籤列表** | GET | `/tags/<tag_name>` | `templates/index.html` | 顯示帶有特定標籤的食譜 |
| **新增食譜頁面** | GET | `/recipes/new` | `templates/recipe_form.html`| 顯示新增表單 |
| **建立食譜** | POST | `/recipes/new` | — | 接收表單與圖片，存入 DB 後重導向 |
| **食譜詳細內容** | GET | `/recipes/<int:id>` | `templates/recipe_detail.html`| 顯示單一食譜圖文與筆記 |
| **編輯食譜頁面** | GET | `/recipes/<int:id>/edit`| `templates/recipe_form.html`| 顯示編輯表單，帶入原資料 |
| **更新食譜** | POST | `/recipes/<int:id>/edit`| — | 接收表單並更新資料庫，重導向 |
| **刪除食譜** | POST | `/recipes/<int:id>/delete`| — | 刪除資料庫該筆食譜，重導向至首頁 |
| **切換我的最愛** | POST | `/recipes/<int:id>/favorite`| — | 切換 `is_favorite` 狀態，重導回原頁面 |
| **更新烹飪筆記** | POST | `/recipes/<int:id>/note`| — | 更新 `note` 欄位，重導回詳細頁 |

*(註：為了減少重複開發，列表相關頁面皆共用 `index.html`，並依據傳入的變數改變頁面標題；新增與編輯則共用 `recipe_form.html`)*

## 2. 每個路由的詳細說明

### 首頁與列表查詢 (`/`, `/search`, `/favorites`, `/tags/<tag_name>`)
*   **輸入**：URL 參數（如 `q` 代表搜尋字串）。
*   **處理邏輯**：使用 `Recipe.query` 過濾出對應的食譜結果（按建立時間降冪排序）。
*   **輸出**：渲染 `index.html`，傳遞 `recipes` 變數與 `page_title`（如「搜尋結果：牛肉」、「我的最愛」）。

### 新增/編輯食譜 (`/recipes/new`, `/recipes/<id>/edit`)
*   **輸入**：表單欄位 (`title`, `content`, `tags` 字串, `image` 檔案)。
*   **處理邏輯 (GET)**：建立空的或帶入既有資料的表單。
*   **處理邏輯 (POST)**：
    1. 若有上傳圖片，使用安全檔名儲存至 `static/uploads/`。
    2. 將輸入的 `tags` 字串（如「中式, 備餐」）切割，尋找或建立對應的 Tag 物件。
    3. 呼叫 Recipe 的 `create` 或 `update` 方法並綁定標籤。
*   **輸出**：成功後重導向至詳細頁 (`/recipes/<id>`) 或首頁。
*   **錯誤處理**：如果必填欄位 (如標題) 空白，返回表單並顯示錯誤訊息。

### 刪除食譜 (`/recipes/<id>/delete`)
*   **處理邏輯**：查詢該 Recipe，並呼叫其 `delete` 方法。同時從檔案系統中移除對應的圖片檔案（如果存在）。
*   **輸出**：重導向至首頁 `/`。

## 3. Jinja2 模板清單

所有的模板檔案將放置於 `app/templates/` 中。

- `base.html`：所有頁面的基礎結構。
  *   包含 `<head>` 區塊、導覽列（Logo、搜尋框、寫食譜按鈕、我的最愛連結）、以及共同的 CSS/JS 引用。
  *   定義 `{% block content %}{% endblock %}` 供子模板填寫。
- `index.html` (繼承 `base.html`)：以卡片網格形式顯示食譜清單。
- `recipe_detail.html` (繼承 `base.html`)：顯示單一食譜的標題、標籤、大圖、食材步驟，以及切換最愛按鈕。下方提供編輯筆記的區塊。
- `recipe_form.html` (繼承 `base.html`)：包含標題、內容、圖片上傳、標籤輸入（以逗號分隔）的表單頁面。

## 4. 路由骨架程式碼
請參考專案 `app/routes/` 裡的 Python 檔案：
- `main_routes.py` (首頁與一般查詢)
- `recipe_routes.py` (食譜的 CRUD 與操作)
- `__init__.py` (Blueprint 註冊邏輯)
