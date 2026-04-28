from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜頁面與建立邏輯。
    GET:
      輸出: 渲染 recipe_form.html
    POST:
      輸入: 表單資料 (title, content, tags, image file)
      處理邏輯: 儲存圖片，解析標籤字串建立 Tag，建立 Recipe 並綁定 Tags。
      輸出: 重導向到首頁
      錯誤處理: 若 title 空白，返回表單顯示錯誤訊息。
    """
    pass

@recipe_bp.route('/<int:id>')
def recipe_detail(id):
    """
    查看食譜詳細資訊。
    輸入: 食譜 ID
    處理邏輯: Recipe.get_by_id(id)
    輸出: 渲染 recipe_detail.html
    錯誤處理: 若找不到該食譜，回傳 404 Not Found 頁面。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜頁面與更新邏輯。
    GET:
      處理邏輯: 取得原有食譜資料
      輸出: 渲染 recipe_form.html (帶入原資料)
    POST:
      輸入: 表單更新資料
      處理邏輯: 更新 Recipe，若有新圖片則覆蓋並刪除舊圖。更新關聯的 Tags。
      輸出: 重導向至該食譜詳細頁
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜。
    輸入: 食譜 ID
    處理邏輯: 刪除對應的 Recipe 物件與相關圖片
    輸出: 重導向至首頁
    """
    pass

@recipe_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    將食譜加入或移除我的最愛。
    輸入: 食譜 ID
    處理邏輯: 反轉 Recipe.is_favorite 狀態
    輸出: 重導向回上一頁 (詳細頁或列表頁)
    """
    pass

@recipe_bp.route('/<int:id>/note', methods=['POST'])
def update_note(id):
    """
    更新食譜的烹飪筆記。
    輸入: 食譜 ID, 表單 note 內容
    處理邏輯: 更新 Recipe.note 欄位
    輸出: 重導向回食譜詳細頁
    """
    pass
