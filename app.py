from flask import Flask, Blueprint, request, make_response, jsonify
from flask_cors import CORS
from passlib.hash import sha256_crypt
import pyodbc

# user_bp = Blueprint("", __name__)
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
    print('Hello World!')
    return make_response(jsonify({'message': 'Hello'}), 200)


@app.route('/user/login', methods=["post"])
def login_user():
    conn, curs = connect_conn()

    if request.is_json:
        user = request.get_json()["user"]

        try:
            curs.execute("SELECT * FROM users WHERE mail = ?", user['mail'])
            row = curs.fetchone()

            while row:
                print("password:" + row[2])
                if sha256_crypt.verify(user["pwd"], row[2]):
                    return make_response(jsonify({'message': 'User Exists'}), 202)
                row = curs.fetchone()

            return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
        except BaseException as e:
            return make_response(jsonify({'message': 'Unknown Error'}), 400)
        finally:
            close_conn(conn)


@app.route('/user/create', methods=["post"])
def create_user():
    conn, curs = connect_conn()

    if request.is_json:
        user = request.get_json()["user"]
        pwd_hash = sha256_crypt.hash(user["pwd"])

        try:
            print("Insert new user:")
            if not check_if_user_exists(curs, user["mail"]):
                curs.execute("INSERT INTO users (name, password, mail) VALUES (?, ?, ?)", user["name"], pwd_hash, user["mail"])
                conn.commit()
                print("Successfully inserted: " + user["name"])
                return make_response(jsonify({'message': 'User created successfully'}), 201)
            else:
                print("User exists")
                return make_response(jsonify({'message': 'User already exists'}), 400)
        except BaseException as e:
            print("Failed inserting user...")
            return make_response(jsonify({'message': 'Unknown Error'}), 400)
        finally:
            close_conn(conn)


def connect_conn():
    conn = pyodbc.connect(connection_string)
    curs = conn.cursor()
    return conn, curs


def close_conn(conn):
    print("Closing connection...")
    conn.close()
    print("Connection closed")


def check_if_user_exists(curs, mail):
    curs.execute("SELECT mail FROM users")
    row = curs.fetchone()

    while row:
        if row[0] == mail:
            return True
        row = curs.fetchone()

    return False




if __name__ == '__main__':
    app.run()
