from flask import Flask

from .user import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
