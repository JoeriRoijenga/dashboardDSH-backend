from flask import Blueprint, request, make_response, jsonify
from passlib.hash import sha256_crypt
from app import connect_conn, close_conn

users_bp = Blueprint("users", __name__)


@users_bp.route('/user/login', methods=["post"])
def login_user():
    conn, curs = connect_conn()

    if request.is_json:
        user = request.get_json()["user"]

        if check_if_user_exists_by_mail(curs, user['mail']):
            try:
                curs.execute("SELECT password FROM users WHERE mail = ?;", user['mail'])
                row = curs.fetchone()

                while row:
                    if sha256_crypt.verify(user["pwd"], row[0]):
                        return make_response(jsonify({'message': 'User Exists'}), 202)
                    row = curs.fetchone()

                return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
            except:
                return make_response(jsonify({'error': 'Unknown Error'}), 400)
            finally:
                close_conn(conn)
        return make_response(jsonify({'error': 'Wrong Credentials'}), 401)
    return make_response(jsonify({'error': 'Wrong Format'}), 400)


@users_bp.route('/user/create', methods=["post"])
def create_user():
    if request.is_json:
        user = request.get_json()["user"]
        pwd_hash = sha256_crypt.hash(user["pwd"])

        try:
            conn, curs = connect_conn()

            if not check_if_user_exists_by_mail(curs, user["mail"]):
                curs.execute("INSERT INTO users (name, password, mail) VALUES (?, ?, ?);", user["name"], pwd_hash,
                             user["mail"])
                conn.commit()
                return make_response(jsonify({'message': 'User created successfully'}), 201)
            return make_response(jsonify({'message': 'User already exists'}), 400)
        except:
            return make_response(jsonify({'error': 'Unknown Error'}), 400)
        finally:
            close_conn(conn)

    return make_response(jsonify({'error': 'Wrong Format'}), 400)


@users_bp.route('/users/get/all', methods=["GET"])
def get_users():
    try:
        conn, curs = connect_conn()

        curs.execute("SELECT name, mail FROM users;")
        users = fetch_all_users(curs)
        return make_response(jsonify({'users': users}), 200)
    except:
        return make_response(jsonify({'message': 'Unknown Error'}), 400)
    finally:
        close_conn(conn)


@users_bp.route('/users/get/<string:_id>', methods=["GET"])
def get_user(_id):
    try:
        conn, curs = connect_conn()

        if check_if_user_exists_by_id(curs, _id):
            curs.execute("SELECT name, mail FROM users WHERE id = ?;", _id)

            return make_response(jsonify({'user': fetch_all_users(curs)}), 200)
        return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
    except:
        return make_response(jsonify({'error': 'Unknown Error'}), 400)
    finally:
        close_conn(conn)


@users_bp.route('/users/update/<string:_id>', methods=["PUT"])
def update_user(_id):
    if request.is_json:
        user = request.get_json()["user"]

        try:
            conn, curs = connect_conn()
            if check_if_user_exists_by_id(curs, _id):
                curs.execute("UPDATE users SET name = ?, mail = ?;", user["name"], user["mail"])
                return make_response(jsonify({'message': 'OK'}), 200)
            return make_response(jsonify({'message': 'User Doesn\'t Exists'}), 401)
        except:
            return make_response(jsonify({'message': 'Unknown Error'}), 400)
        finally:
            close_conn(conn)

    return make_response(jsonify({'message': 'Wrong Format'}), 400)


def fetch_all_users(curs):
    dictionary = {}
    row = curs.fetchone()
    count = 0

    while row:
        dictionary[count] = {'name': row[0], 'mail': row[1]}
        row = curs.fetchone()
        count += 1

    return dictionary


def check_if_user_exists_by_id(curs, _id):
    return True if curs.execute("SELECT COUNT(id) FROM users WHERE id = ?", _id).fetchone()[0] == 1 else False


def check_if_user_exists_by_mail(curs, mail):
    return True if curs.execute("SELECT COUNT(mail) FROM users WHERE mail = ?", mail).fetchone()[0] == 1 else False
