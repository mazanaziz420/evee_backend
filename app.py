from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = b'_5#y2L"F4    Q8z\n\xec]/'

from users import user_bp

app.register_blueprint(user_bp)
mail = Mail(app)


def create_app(config):
    return app


if __name__ == '__main__':
    app.run(debug=True)
