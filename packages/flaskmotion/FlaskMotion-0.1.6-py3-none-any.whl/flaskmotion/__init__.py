from flask import Blueprint, render_template, current_app, send_from_directory
import os

class FlaskMotion:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.blueprint = Blueprint(
            'flaskmotion',
            __name__,
            static_folder='static',
            template_folder='templates'
        )
        app.register_blueprint(self.blueprint, url_prefix='/flaskmotion')

        @self.blueprint.context_processor
        def inject_flaskmotion_assets():
            return dict(
                flaskmotion_css_url='/flaskmotion/static/css/flaskmotion.css',
                flaskmotion_js_url='/flaskmotion/static/js/flaskmotion.js'
            )
