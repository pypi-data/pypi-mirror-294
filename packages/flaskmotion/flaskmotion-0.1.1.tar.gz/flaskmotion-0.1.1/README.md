# FlaskMotion

FlaskMotion is a lightweight Flask extension that adds smooth page transitions (fade-in, fade-out) to your Flask web applications.

## Usage

1. Import and initialize FlaskMotion in your Flask application:

```python
from flask import Flask
from flaskmotion import FlaskMotion

app = Flask(__name__)
FlaskMotion(app)

if __name__ == '__main__':
    app.run()
