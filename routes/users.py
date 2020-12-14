from flask import Blueprint, request, make_response, jsonify
from passlib.hash import sha256_crypt
from connection_settings import connect, close

users_bp = Blueprint("users", __name__)


@users_bp.route('/login', methods=["post"])
def login_user():
    connection, cursor = connect()

    if request.is_json:
        user = request.get_json()["user"]

        if check_if_user_exists_by_mail(cursor, user['mail']):
            try:
                cursor.execute("SELECT password FROM users WHERE mail = ?;", user['mail'])
                row = cursor.fetchone()

                while row:
                    if sha256_crypt.verify(user["pwd"], row[0]):
                        return make_response(jsonify({'message': 'User Exists'}), 202)
                    row = cursor.fetchone()

                return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
            except:
                return make_response(jsonify({'error': 'Unknown Error'}), 400)
            finally:
                close(connection)
        return make_response(jsonify({'error': 'Wrong Credentials'}), 401)
    return make_response(jsonify({'error': 'Wrong Format'}), 400)


@users_bp.route('/create', methods=["post"])
def create_user():
    if request.is_json:
        user = request.get_json()["user"]
        pwd_hash = sha256_crypt.hash(user["pwd"])

        try:
            connection, cursor = connect()

            if not check_if_user_exists_by_mail(cursor, user["mail"]):
                cursor.execute("INSERT INTO users (name, password, mail) VALUES (?, ?, ?);", user["name"], pwd_hash,
                             user["mail"])
                connection.commit()
                return make_response(jsonify({'message': 'User created successfully'}), 201)
            return make_response(jsonify({'message': 'User already exists'}), 400)
        except:
            return make_response(jsonify({'error': 'Unknown Error'}), 400)
        finally:
            close(connection)

    return make_response(jsonify({'error': 'Wrong Format'}), 400)


@users_bp.route('/get/all', methods=["GET"])
def get_users():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT name, mail FROM users;")
        users = fetch_all_users(cursor)
        return make_response(jsonify({'users': users}), 200)
    except:
        return make_response(jsonify({'message': 'Unknown Error'}), 400)
    finally:
        close(connection)


@users_bp.route('/get/<string:_id>', methods=["GET"])
def get_user(_id):
    try:
        connection, cursor = connect()

        if check_if_user_exists_by_id(cursor, _id):
            cursor.execute("SELECT name, mail FROM users WHERE id = ?;", _id)

            return make_response(jsonify({'user': fetch_all_users(cursor)}), 200)
        return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
    except:
        return make_response(jsonify({'error': 'Unknown Error'}), 400)
    finally:
        close(connection)


@users_bp.route('/update/<string:_id>', methods=["PUT"])
def update_user(_id):
    if request.is_json:
        user = request.get_json()["user"]

        try:
            connection, cursor = connect()
            if check_if_user_exists_by_id(cursor, _id):
                cursor.execute("UPDATE users SET name = ?, mail = ?;", user["name"], user["mail"])
                return make_response(jsonify({'message': 'OK'}), 200)
            return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
        except:
            return make_response(jsonify({'message': 'Unknown Error'}), 400)
        finally:
            close(connection)

    return make_response(jsonify({'message': 'Wrong Format'}), 400)


def fetch_all_users(cursor):
    dictionary = {}
    row = cursor.fetchone()
    count = 0

    while row:
        dictionary[count] = {'name': row[0], 'mail': row[1]}
        row = cursor.fetchone()
        count += 1

    return dictionary


def check_if_user_exists_by_id(cursor, _id):
    return True if cursor.execute("SELECT COUNT(id) FROM users WHERE id = ?", _id).fetchone()[0] == 1 else False


def check_if_user_exists_by_mail(cursor, mail):
    return True if cursor.execute("SELECT COUNT(mail) FROM users WHERE mail = ?", mail).fetchone()[0] == 1 else False
