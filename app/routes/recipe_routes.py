import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.models.recipe import Recipe
from app.models.tag import Tag
from app.models import db

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """新增食譜頁面與建立邏輯"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags_input = request.form.get('tags', '').strip()
        image_file = request.files.get('image')

        # 驗證必填欄位
        if not title:
            flash('食譜標題為必填欄位！', 'danger')
            return render_template('recipe_form.html', form_data=request.form)

        # 處理圖片上傳
        image_path = None
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                # 加上 UUID 避免檔名重複覆蓋
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                image_file.save(os.path.join(upload_folder, unique_filename))
                image_path = f"uploads/{unique_filename}"
            else:
                flash('不支援的圖片格式！請上傳 png, jpg, jpeg, gif 或 webp。', 'danger')
                return render_template('recipe_form.html', form_data=request.form)

        # 建立食譜
        recipe = Recipe(title=title, content=content, image_path=image_path)
        
        # 處理標籤
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag = Tag.get_or_create(name)
                if tag:
                    recipe.tags.append(tag)
                    
        recipe.create()
        flash('食譜新增成功！', 'success')
        return redirect(url_for('main.index'))

    # GET 請求：顯示空白表單
    return render_template('recipe_form.html', form_data={})

@recipe_bp.route('/<int:id>')
def recipe_detail(id):
    """查看單一食譜詳細資訊"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('main.index'))
    return render_template('recipe_detail.html', recipe=recipe)

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """編輯食譜頁面與更新邏輯"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags_input = request.form.get('tags', '').strip()
        image_file = request.files.get('image')

        if not title:
            flash('食譜標題為必填欄位！', 'danger')
            form_data = request.form.to_dict()
            form_data['tags_str'] = tags_input
            return render_template('recipe_form.html', recipe=recipe, form_data=form_data)

        # 更新基本資料
        recipe.title = title
        recipe.content = content

        # 處理新圖片上傳
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # 刪除舊圖片避免佔用空間
                if recipe.image_path:
                    old_path = os.path.join(current_app.root_path, 'static', recipe.image_path)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except OSError:
                            pass # 檔案可能已被刪除或沒有權限
                            
                filename = secure_filename(image_file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                image_file.save(os.path.join(upload_folder, unique_filename))
                recipe.image_path = f"uploads/{unique_filename}"
            else:
                flash('不支援的圖片格式！', 'danger')
                form_data = request.form.to_dict()
                form_data['tags_str'] = tags_input
                return render_template('recipe_form.html', recipe=recipe, form_data=form_data)

        # 處理標籤更新
        recipe.tags.clear()
        if tags_input:
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag = Tag.get_or_create(name)
                if tag:
                    recipe.tags.append(tag)

        db.session.commit()
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipe.recipe_detail', id=recipe.id))

    # GET 請求：準備表單預設值
    form_data = {
        'title': recipe.title,
        'content': recipe.content,
        'tags_str': ', '.join([t.name for t in recipe.tags])
    }
    return render_template('recipe_form.html', recipe=recipe, form_data=form_data)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """刪除食譜"""
    recipe = Recipe.get_by_id(id)
    if recipe:
        # 刪除關聯的圖片檔案
        if recipe.image_path:
            old_path = os.path.join(current_app.root_path, 'static', recipe.image_path)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass
        recipe.delete()
        flash('食譜已成功刪除。', 'success')
    else:
        flash('找不到該食譜！', 'danger')
    return redirect(url_for('main.index'))

@recipe_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """將食譜加入或移除我的最愛"""
    recipe = Recipe.get_by_id(id)
    if recipe:
        recipe.is_favorite = not recipe.is_favorite
        db.session.commit()
        status = "加入" if recipe.is_favorite else "移除"
        flash(f'已將食譜{status}我的最愛！', 'success')
        # 嘗試導回上一頁，若無則回詳細頁
        return redirect(request.referrer or url_for('recipe.recipe_detail', id=recipe.id))
    
    flash('找不到該食譜！', 'danger')
    return redirect(url_for('main.index'))

@recipe_bp.route('/<int:id>/note', methods=['POST'])
def update_note(id):
    """更新食譜的烹飪筆記"""
    recipe = Recipe.get_by_id(id)
    if recipe:
        note = request.form.get('note', '').strip()
        recipe.note = note
        db.session.commit()
        flash('烹飪筆記已更新！', 'success')
        return redirect(url_for('recipe.recipe_detail', id=recipe.id))
        
    flash('找不到該食譜！', 'danger')
    return redirect(url_for('main.index'))
