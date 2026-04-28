from flask import Blueprint, render_template, request
from app.models.recipe import Recipe
from app.models.tag import Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """顯示首頁的所有食譜列表"""
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes, page_title="所有食譜")

@main_bp.route('/search')
def search():
    """搜尋食譜標題或內容"""
    query = request.args.get('q', '').strip()
    if query:
        # 簡單的 LIKE 搜尋，比對標題或內容
        recipes = Recipe.query.filter(
            (Recipe.title.ilike(f'%{query}%')) | (Recipe.content.ilike(f'%{query}%'))
        ).order_by(Recipe.created_at.desc()).all()
        page_title = f'搜尋結果：{query}'
    else:
        recipes = Recipe.get_all()
        page_title = "所有食譜"
        query = ""
    return render_template('index.html', recipes=recipes, page_title=page_title, search_query=query)

@main_bp.route('/favorites')
def favorites():
    """顯示我的最愛清單"""
    recipes = Recipe.query.filter_by(is_favorite=True).order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes, page_title="我的最愛")

@main_bp.route('/tags/<tag_name>')
def tag_filter(tag_name):
    """顯示特定標籤的食譜"""
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        recipes = []
        page_title = f'找不到標籤：{tag_name}'
    else:
        recipes = tag.recipes
        # 將 recipes 按照建立時間降冪排序
        recipes = sorted(recipes, key=lambda x: x.created_at, reverse=True)
        page_title = f'標籤：{tag_name}'
        
    return render_template('index.html', recipes=recipes, page_title=page_title)
