from flask import Flask, Blueprint, request, make_response, jsonify
from flask_cors import CORS
import pyodbc

from routes import users_bp

app = Flask(__name__)
CORS(app)

driver = "{ODBC Driver 17 for SQL Server}"
server = "tcp:iot-db-roijenga.database.windows.net,1433"
database = "iot-db-weather-pi"
username = "iot-joeri-roijenga"
password = "cO1WfBYif7eA"
encryption = "yes"
certificate = "no"
timeout = "30"

connection_string = 'Driver=%s;Server=%s;Database=%s;Uid=%s;Pwd=%s;Encrypt=%s;TrustServerCertificate=%s;Connection Timeout=%s;' % (
    driver, server, database, username, password, encryption, certificate, timeout)


@app.route('/', methods=["post"])
def hello_world():
    return make_response(jsonify({'message': 'Hello World'}), 200)


def connect_conn():
    conn = pyodbc.connect(connection_string)
    curs = conn.cursor()
    return conn, curs


def close_conn(conn):
    conn.close()


def register_blueprints():
    app.register_blueprint(users_bp, url_prefix="/users")


if __name__ == '__main__':
    register_blueprints()
    app.run()
