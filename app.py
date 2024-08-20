from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.users_bp import users_bp
from models import init_app

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

init_app(app)

app.register_blueprint(users_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
