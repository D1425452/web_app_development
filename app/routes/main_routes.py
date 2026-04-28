from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁的所有食譜列表。
    輸入: 無
    處理邏輯: 呼叫 Recipe.get_all()
    輸出: 渲染 index.html
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋食譜標題或內容。
    輸入: GET 參數 ?q=keyword
    處理邏輯: 使用關鍵字 query 資料庫，以 LIKE 比對 title 或 content
    輸出: 渲染 index.html (顯示搜尋結果)
    """
    pass

@main_bp.route('/favorites')
def favorites():
    """
    顯示我的最愛清單。
    輸入: 無
    處理邏輯: 查詢 is_favorite == True 的食譜
    輸出: 渲染 index.html (顯示最愛結果)
    """
    pass

@main_bp.route('/tags/<tag_name>')
def tag_filter(tag_name):
    """
    顯示特定標籤的食譜。
    輸入: URL 變數 tag_name
    處理邏輯: 尋找該名稱的 Tag，並取出對應的 recipes
    輸出: 渲染 index.html (顯示標籤過濾結果)
    錯誤處理: 找不到標籤則回傳 404 或顯示空列表
    """
    pass
