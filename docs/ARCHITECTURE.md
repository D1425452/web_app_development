# 系統架構文件 (ARCHITECTURE)

基於「食譜收藏系統」的需求，本系統將採用輕量化架構，以 Python Flask 作為核心框架，搭配 SQLite 作為資料庫，提供一個穩定且容易開發維護的個人化應用服務。

## 1. 技術架構說明

*   **選用技術與原因**：
    *   **後端框架：Python + Flask**
        Flask 輕量、靈活且學習曲線平緩，沒有繁重的不必要組件，非常適合中小型應用與個人專案。能快速實作所需的 CRUD 功能。
    *   **前端渲染：Jinja2 樣板引擎**
        遵循需求，不採用前後端分離，直接讓 Flask 搭配 Jinja2 進行伺服器端渲染 (SSR)。省下定義 API 與管理前端專案的時間，能最快速產出 MVP。
    *   **資料庫：SQLite**
        輕量化關聯式資料庫，資料存放在實體檔案中，不需要建立或維護資料庫伺服器，完全符合個人專屬系統的情境。
    *   **資料庫存取：Flask-SQLAlchemy (ORM)**
        採用 ORM 以 Python 物件的操作方式來存取資料。提升程式碼可讀性及維護性，也能有效防範基本的 SQL Injection 攻擊。

*   **Flask MVC 模式說明**：
    雖然 Flask 本身不嚴格限制架構，但本專案將遵循常見的 MVC (Model-View-Controller) 概念來組織程式碼：
    *   **Model (模型)**：負責定義資料庫表格結構（如 Recipe, Tag 等）與處理資料的讀寫。
    *   **View (視圖)**：負責呈現畫面給使用者，在此專案中即是 Jinja2 渲染的 HTML 樣板。
    *   **Controller (控制器)**：由 Flask 的路由 (Routes) 擔任，負責接收使用者的請求、向 Model 獲取或更新資料，最後將資料傳遞給 View 來產生網頁。

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
└── app.py                    ← 專案啟動的入口程式
```

---

## 3. 元件關係圖

以下圖表示出當使用者發出請求時，系統內部元件的交互關係：

```mermaid
flowchart TD
    User([瀏覽器 / 使用者]) <-->|HTTP 請求 / 回應| Route[Flask Route\n(Controller)]
    
    subgraph 後端伺服器 (Flask)
        Route <-->|向 Model 查詢/更新資料| Model[Model\n(Flask-SQLAlchemy)]
        Route -->|傳遞資料並渲染| Template[Jinja2 Template\n(View)]
        Template -->|產出 HTML| Route
    end
    
    subgraph 資料層
        Model <-->|讀寫資料| SQLite[(SQLite 資料庫)]
    end
```

這張圖呈現了完整的資料流：
1. **瀏覽器**發送請求給 **Flask Route**。
2. **Flask Route** 向 **Model** 請求資料。
3. **Model** 與 **SQLite** 溝通取得資料。
4. **Flask Route** 將資料送給 **Jinja2 Template** 渲染畫面。
5. 最終由 **Flask Route** 將產生的網頁回傳給**瀏覽器**。

---

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (SSR) 而非前後端分離**
   * **決策原因**：由於系統定位為個人收藏工具，選用 Jinja2 的 SSR 模式可以將路由與頁面綑綁在一起開發，能快速產出完整功能，不需要花時間維護獨立的前端專案與設計 REST API。
   
2. **圖片儲存於本機資料夾 (`static/uploads/`) 而非資料庫**
   * **決策原因**：直接將圖檔寫入 SQLite 會造成資料庫檔案極速膨脹且拖慢查詢效能。將圖片存在靜態資料夾中，資料庫僅記錄「檔案路徑」，能兼顧網頁載入效能與資料庫輕量化。

3. **使用 SQLAlchemy ORM 作為資料互動層**
   * **決策原因**：食譜設計上會涉及「多對多」的情境（如食譜與標籤的關係）。使用 ORM 可以很優雅地管理關聯表，也內建防止 SQL Injection 的安全機制，且 Python 物件導向語法讓程式碼更好讀、好維護。

4. **採用資料夾結構切分 Model, View, Controller**
   * **決策原因**：即使是小型專案，將路由 (`routes.py`)、資料模型 (`models.py`) 與頁面 (`templates/`) 獨立分開，可以讓程式碼架構非常清晰。當後續要擴充功能時（例如加入搜尋或分類），能輕易找到對應的邏輯區塊修改。
