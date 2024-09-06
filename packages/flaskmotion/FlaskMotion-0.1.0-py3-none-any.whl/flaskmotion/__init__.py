from flask import Blueprint, render_template

def FlaskMotion(app):
    # Register the static folder to allow serving CSS/JS
    app.register_blueprint(flaskmotion_bp)

flaskmotion_bp = Blueprint(
    'flaskmotion',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/flaskmotion'
)
