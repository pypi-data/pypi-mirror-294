from flask import Blueprint, render_template

bp = Blueprint('flaskmotion', __name__, template_folder='templates', static_folder='static')

@bp.before_app_first_request
def add_default_styles_and_scripts():
    """Ensure the default CSS and JS are available."""
    pass  # No code needed, just a placeholder

# Optionally, you can define additional routes or functions here
