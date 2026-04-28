from .main_routes import main_bp
from .recipe_routes import recipe_bp

def register_blueprints(app):
    """
    將所有的 Blueprint 註冊到 Flask 應用程式。
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
