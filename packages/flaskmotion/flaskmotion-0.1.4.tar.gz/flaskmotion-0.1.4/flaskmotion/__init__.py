# flaskmotion/__init__.py

from flask import Blueprint, render_template, send_from_directory
import os

# Define the Blueprint
bp = Blueprint('flaskmotion', __name__, static_folder='static', template_folder='templates')

# Define the FlaskMotion class or function if required
class FlaskMotion:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(bp)

@bp.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static'), filename)

@bp.route('/')
def index():
    return render_template('index.html')
