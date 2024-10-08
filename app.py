from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Import CORS
from config import Config
from routes.users_bp import users_bp
from routes.venue_provider_bp import venue_provider_bp
from models import init_app

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

jwt = JWTManager(app)

init_app(app)

app.register_blueprint(users_bp, url_prefix='/')
app.register_blueprint(venue_provider_bp, url_prefix='/venueProvider')

if __name__ == '__main__':
    app.run(debug=True)
