class FlaskMotion:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Register the static files
        @app.context_processor
        def inject_flaskmotion():
            return dict(fade_in_class='flaskmotion-fade-in', fade_out_class='flaskmotion-fade-out')
        
        # You can also register the routes or templates if needed
