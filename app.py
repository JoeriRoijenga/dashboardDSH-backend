from flask import Flask
from flask_cors import CORS

from routes import users_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "0BB00075E0A451F529A02D3F5EB73F1FE8CC80016AD8BDCF71159533164267E-random-key"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)
blacklist = set()

app.config['blacklist'] = blacklist
app.config['jwt'] = jwt

CORS(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    print(jti in blacklist)
    return jti in blacklist

def register_blueprints():
    app.register_blueprint(users_bp, url_prefix="/users")


if __name__ == '__main__':
    register_blueprints()
    app.run()
