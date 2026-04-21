# 系統架構文件 (ARCHITECTURE)

基於「食譜收藏系統」的需求，本系統將採用輕量化架構，以 Python Flask 作為核心框架，搭配 SQLite 作為資料庫，提供一個穩定且容易開發維護的個人化應用服務。

## 1. 技術架構說明

### 選用技術與原因

*   **後端框架：Python Flask**
    *   **原因**：Flask 輕量、靈活且學習曲線平緩，非常適合中小型應用與個人專案。其內建的路由及許多實用的擴充套件，能快速實作所需的 CRUD 功能。
*   **前端渲染：Jinja2 樣板引擎**
    *   **原因**：遵循 PRD 架構要求，不採用前後端分離，直接讓 Flask 搭配 Jinja2 進行伺服器端渲染 (SSR)。這樣可以大幅省下定義 API 與管理前端專案的時間，能最快速產出 MVP。
*   **資料庫：SQLite**
    *   **原因**：輕量化關聯式資料庫，資料存放在實體檔案中，不需要建立或維護資料庫伺服器，備份也相當容易，完全符合個人專屬系統的情境。
*   **資料庫存取：Flask-SQLAlchemy (ORM)**
    *   **原因**：採用 ORM 以 Python 物件的操作方式來存取資料。除了能提升程式碼的可讀性及維護性外，也能有效防範基本的 SQL Injection 攻擊，符合 PRD 中提及的安全準則。

---

## 2. 專案資料夾結構

以下是本專案建議的資料夾結構與各元件負責的用途：

```text
web_app_development/
├── app/                      ← 應用程式主目錄
│   ├── __init__.py           ← Flask App 初始化、套件與資料庫配置
│   ├── models.py             ← 資料庫模型 (Models - 如 Recipe, Tag 等)
│   ├── routes.py             ← Flask 路由與視圖邏輯 (Controllers)
│   ├── templates/            ← Jinja2 HTML 樣板 (Views)
│   │   ├── base.html         ← 共同基礎版型 (包含導覽列等)
│   │   ├── index.html        ← 首頁/食譜列表瀏覽頁面
│   │   ├── recipe_detail.html← 食譜詳細資訊、圖片與烹飪筆記展示頁
│   │   └── recipe_form.html  ← 食譜新增/編輯表單頁面
│   └── static/               ← 靜態資源目錄
│       ├── css/              ← 網站樣式表 (style.css)
│       ├── js/               ← 前端互動腳本 (script.js)
│       └── uploads/          ← 使用者上傳的食譜圖片存放區
├── instance/                 ← 實例專屬的資料夾 (建議加入 .gitignore)
│   └── database.db           ← SQLite 資料庫實體檔案
├── docs/                     ← 專案文件存放區
│   ├── PRD.md                ← 產品需求文件
│   └── ARCHITECTURE.md       ← 系統架構設計文件 (本文件)
├── requirements.txt          ← Python 套件依賴清單
├── .gitignore                ← Git 忽略名單 (排除圖檔、資料庫及快取)
└── run.py                    ← 專案啟動的入口程式
```

---

## 3. 元件關係圖

以下圖表示出當使用者發出請求時，系統內部元件的交互關係：

```mermaid
flowchart TD
    User([使用者 / 瀏覽器]) <-->|HTTP Request / Response| FlaskRoute[Flask Route\n(Controller)]
    
    subgraph 後端伺服器 (Flask)
        FlaskRoute <-->|新增 / 查詢 / 刪除| Model[Model\n(Flask-SQLAlchemy)]
        FlaskRoute -->|準備資料並渲染| Template[Jinja2 Template\n(View)]
        Template -->|產出完整 HTML 結果| FlaskRoute
    end
    
    subgraph 資料層
        Model <-->|執行 SQL 指令| SQLite[(SQLite Database)]
    end
    
    subgraph 靜態與檔案處理
        FlaskRoute <-->|儲存與讀取圖片| FileSystem[Static / Uploads\n(本機檔案系統)]
    end
```

---

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (SSR)**
   * **決策原因**：由於系統定位為個人收藏工具，畫面的複雜度並不高（主要是列表瀏覽及表單填寫）。選用 Jinja2 的 SSR 模式可以將路由與頁面綑綁在一起，避免開發時因為前後端分離而需要耗費心力去串接與設計大量 RESTful API。
   
2. **圖片儲存於本機檔案系統而非資料庫**
   * **決策原因**：食譜往往伴隨精美的圖片，若直接將二進位圖檔 (Blobs) 寫入 SQLite 會造成資料庫檔案極速膨脹且拖慢查詢效能。因此將圖檔存在 `app/static/uploads` 中，而資料庫僅儲存「檔案路徑字串」，能兼顧效能與備份彈性。

3. **使用 SQLAlchemy 作為資料互動層**
   * **決策原因**：由於食譜設計上會涉及「多對多」的情境（例如：一個食譜會有多個標籤，一個標籤也會包含多個食譜），直接寫原生 SQL 語句在處理關聯表時易產生錯誤。使用 ORM 可以很優雅地管理關聯表，也內建防止 SQL Injection 的安全機制。

4. **採用簡單的 Application Factory 模式 (模組化設計)**
   * **決策原因**：將 `app` 置於專屬的套件資料夾中，並將初始化抽離至 `__init__.py` 中，而不是全部擠在一個 `app.py` 中。這樣不僅使得專案結構乾淨，也便於之後分離 models 和 routes，降低程式碼的耦合度與維護成本。
