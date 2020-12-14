from flask import Flask, make_response, jsonify
from flask_cors import CORS

from routes import users_bp

app = Flask(__name__)
CORS(app)


def register_blueprints():
    app.register_blueprint(users_bp, url_prefix="/users")


if __name__ == '__main__':
    register_blueprints()
    app.run()
