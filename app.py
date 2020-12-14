from flask import Flask, make_response, jsonify
from flask_cors import CORS

from routes import users_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "0BB00075E0A451F529A02D3F5EB73F1FE8CC80016AD8BDCF71159533164267E-random-key"
jwt = JWTManager(app)

CORS(app)


def register_blueprints():
    app.register_blueprint(users_bp, url_prefix="/users")


if __name__ == '__main__':
    register_blueprints()
    app.run()
