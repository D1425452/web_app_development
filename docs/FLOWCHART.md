# 流程圖設計 (Flowchart)

本文件根據產品需求文件 (PRD) 與系統架構設計 (ARCHITECTURE)，視覺化使用者的操作流程與系統內部的資料流動。

## 1. 使用者流程圖 (User Flow)

此流程圖展示使用者進入系統後，可以進行的各項操作路徑。包含首頁瀏覽、搜尋、分類篩選、以及食譜的 CRUD (新增、查看、修改、刪除) 流程。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁 - 食譜列表]
    
    %% 首頁操作
    Home -->|點擊新增| CreateForm[新增食譜表單]
    Home -->|輸入關鍵字| Search[搜尋結果頁面]
    Home -->|點擊標籤| TagFilter[標籤分類頁面]
    Home -->|點擊我的最愛| Favorites[我的最愛列表]
    
    %% 新增食譜
    CreateForm -->|填寫資訊與上傳圖片| SaveCreate{儲存食譜?}
    SaveCreate -->|成功| Home
    SaveCreate -->|取消| Home
    
    %% 查看詳細與後續操作
    Home -->|點擊單一食譜| Detail[食譜詳細內容頁]
    Search -->|點擊單一食譜| Detail
    TagFilter -->|點擊單一食譜| Detail
    Favorites -->|點擊單一食譜| Detail
    
    %% 詳細頁操作
    Detail -->|點擊編輯| EditForm[編輯食譜表單]
    Detail -->|點擊刪除| Delete{確認刪除?}
    Detail -->|點擊愛心| ToggleFav[加入/移除最愛]
    Detail -->|編輯筆記| UpdateNote[儲存烹飪筆記]
    
    %% 編輯與刪除流程
    EditForm -->|修改完成| SaveEdit{儲存修改?}
    SaveEdit -->|成功| Detail
    SaveEdit -->|取消| Detail
    Delete -->|確認| Home
    Delete -->|取消| Detail
    ToggleFav --> Detail
    UpdateNote --> Detail
```

## 2. 系統序列圖 (Sequence Diagram)

此圖以「**使用者新增包含圖片的食譜**」為例，展示前端瀏覽器、後端 Flask 路由、資料庫模型與 SQLite 之間的互動時序。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant FS as 檔案系統 (uploads)
    participant Model as SQLAlchemy
    participant DB as SQLite

    User->>Browser: 填寫食譜內容並選擇圖片，點擊「儲存」
    Browser->>Route: POST /recipes/new (Form Data)
    
    %% 處理圖片
    Route->>FS: 儲存圖片檔案
    FS-->>Route: 回傳圖片儲存路徑
    
    %% 處理資料庫
    Route->>Model: 建立 Recipe 物件 (包含圖片路徑)
    Model->>DB: 執行 INSERT 語法
    DB-->>Model: 資料寫入成功
    Model-->>Route: 回傳成功狀態
    
    %% 回應前端
    Route-->>Browser: HTTP 302 重導向至首頁 (/)
    Browser->>User: 顯示最新食譜列表
```

## 3. 功能清單對照表

以下整理了所有的核心功能對應的 URL 路徑與 HTTP 方法，為接下來的路由設計提供明確的指引（註：由於 HTML 表單原生僅支援 GET 與 POST，故編輯與刪除皆採用 POST 方法實作）。

| 功能項目 | 說明 | HTTP 方法 | URL 路徑 |
| :--- | :--- | :---: | :--- |
| **食譜列表** | 顯示所有食譜 (首頁) | `GET` | `/` |
| **新增食譜 (表單)** | 顯示新增食譜的頁面 | `GET` | `/recipes/new` |
| **新增食譜 (儲存)** | 接收表單資料並存入資料庫 | `POST` | `/recipes/new` |
| **食譜詳細內容** | 查看單一食譜的圖文與步驟 | `GET` | `/recipes/<id>` |
| **編輯食譜 (表單)** | 顯示編輯食譜的頁面 | `GET` | `/recipes/<id>/edit` |
| **編輯食譜 (儲存)** | 接收修改後的資料並更新 | `POST` | `/recipes/<id>/edit` |
| **刪除食譜** | 從資料庫中刪除該食譜 | `POST` | `/recipes/<id>/delete` |
| **標籤篩選** | 顯示特定標籤下的所有食譜 | `GET` | `/tags/<tag_name>` |
| **關鍵字搜尋** | 依據輸入的關鍵字顯示結果 | `GET` | `/search` |
| **我的最愛列表** | 顯示已收藏的食譜 | `GET` | `/favorites` |
| **切換我的最愛** | 將食譜加入或移除我的最愛 | `POST` | `/recipes/<id>/favorite` |
| **更新烹飪筆記** | 儲存該食譜專屬的烹飪筆記 | `POST` | `/recipes/<id>/note` |
