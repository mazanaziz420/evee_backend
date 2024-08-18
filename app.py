from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from setting import *
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = b'_5#y2L"F4    Q8z\n\xec]/'

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

from users import user_bp

app.register_blueprint(user_bp)
mail = Mail(app)


def create_app(config):
    return app


if __name__ == '__main__':
    app.run(debug=True)
