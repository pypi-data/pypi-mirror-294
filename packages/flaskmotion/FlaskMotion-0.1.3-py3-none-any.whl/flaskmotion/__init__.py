# flaskmotion/__init__.py

from flask import Blueprint, current_app, request, render_template, send_from_directory
import os

bp = Blueprint('flaskmotion', __name__, static_folder='static', template_folder='templates')

@bp.before_app_request
def before_request():
    # Your logic here, if any
    pass

@bp.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static'), filename)

@bp.route('/')
def index():
    return render_template('index.html')
