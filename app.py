from flask import Flask, Blueprint, request
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
    return "hello"


@app.route('/user/create', methods=["post"])
def create_user():
    conn = pyodbc.connect(connection_string)
    curs = conn.cursor()

    #
    # print("Select:")
    # curs.execute("SELECT * FROM users")
    # row = curs.fetchone()
    #
    # while row:
    #     print(row)
    #     row = curs.fetchone()
    #
    # password = sha256_crypt.encrypt("password")
    # password2 = sha256_crypt.encrypt("password")
    #
    # print(password)
    # print(password2)
    #
    # print(sha256_crypt.verify("password", password))

    if request.is_json:
        user = request.get_json()["user"]
        pwd_hash = sha256_crypt.hash(user["password"])
        # print(user["username"])
        # print(user["password"])
        # print(pwd_hash)
        # print(sha256_crypt.verify(user["password"], pwd_hash))

        try:
            print("Insert new user:")
            curs.execute("INSERT INTO users (name ,password, mail) VALUES (?,?,?)", user["username"], pwd_hash,
                         user["mail"])
            if conn.commit():
                print("Successfully inserted: " + curs.fetchone()[0])
        except:
            print("Failed inserting user:")
        finally:
            print("Closing connection...")
            if conn.close():
                print("Connection closed")

    return ""


if __name__ == '__main__':
    app.run()
