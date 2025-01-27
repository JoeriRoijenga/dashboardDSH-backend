from flask import Blueprint, request, jsonify, current_app
from passlib.hash import sha256_crypt
from connection_settings import connect, close
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token, \
    jwt_refresh_token_required, get_raw_jwt, get_jti
 
users_bp = Blueprint("users", __name__)

@users_bp.route('/login', methods=["post"])
def login_user():
    connection = None

    if request.is_json:
        user = request.get_json()
        
        try:
            connection, cursor = connect()

            if check_if_user_exists_by_mail(cursor, user['mail']):
                cursor.execute("SELECT id, name, password, admin FROM users WHERE mail = ?;", user['mail'])
                row = cursor.fetchone()

                while row:
                    if sha256_crypt.verify(user["pwd"], row[2]):
                        tokens = {
                            'access_token': create_access_token(identity={'id': row[0], 'user': row[1], 'mail': user['mail'], 'admin': row[3]}),
                            'refresh_token': create_refresh_token(identity={'id': row[0], 'user': row[1], 'mail': user['mail'], 'admin': row[3]})
                        }

                        return jsonify({'tokens': tokens}), 200
                    row = cursor.fetchone()
                    
                return jsonify({'error': 'User Doesn\'t Exists'}), 401
            return jsonify({'error': 'Wrong Credentials'}), 401
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            if connection is not None:
                close(connection)
    return jsonify({'error': 'Wrong Format'}), 400


@users_bp.route('/logout', methods=["post"])
@jwt_required
def logout_user():
    blacklist = current_app.config['blacklist']
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)

    if request.is_json and len(request.get_json()) != 0:
        token = request.get_json()["token"]
        blacklist.add(get_jti(token))

    return jsonify({"msg": "Successfully logged out"}), 200


@users_bp.route('/create', methods=["post"])
def create_user():
    connection = None

    if request.is_json:
        user = request.get_json()
        pwd_hash = sha256_crypt.hash(user["pwd"])

        try:
            connection, cursor = connect()

            if not check_if_user_exists_by_mail(cursor, user["mail"]):
                cursor.execute("INSERT INTO users (name, password, mail, admin) VALUES (?, ?, ?, ?);", user["name"], pwd_hash, user["mail"], user["admin"])
                connection.commit()
                return jsonify({'message': 'User created successfully'}), 201
            return jsonify({'message': 'User already exists'}), 400
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            if connection is not None:
                close(connection)

    return jsonify({'error': 'Wrong Format'}), 400


@users_bp.route('/delete/<string:_id>', methods=["DELETE"])
@jwt_required
def delete_user(_id):
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("DELETE FROM users WHERE \"id\" = ?;", _id)
        connection.commit()
        
        return jsonify({'message': "success"}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)


@users_bp.route('/get/all', methods=["GET"])
@jwt_required
def get_users():
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("SELECT id, name, mail, admin FROM users;")
        users = fetch_all_users(cursor)
        return jsonify({'users': users}), 200
    except:
        return jsonify({'message': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)


@users_bp.route('/get/<string:_id>', methods=["GET"])
@jwt_required
def get_user(_id):
    connection = None

    try:
        connection, cursor = connect()

        if check_if_user_exists_by_id(cursor, _id):
            cursor.execute("SELECT id, name, mail, admin FROM users WHERE id = ?;", _id)

            return jsonify({'user': fetch_all_users(cursor)}), 200
        return jsonify({'message': 'User Doesn\'t Exists'}), 401
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
                close(connection)

@users_bp.route('/update/<string:_id>', methods=["PUT"])
@jwt_required
def update_user(_id):
    connection = None

    if request.is_json:
        user = request.get_json()

        try:
            connection, cursor = connect()
            if check_if_user_exists_by_id(cursor, _id):
                if "pwd" in user:
                    cursor.execute("UPDATE users SET name = ?, mail = ?, admin = ?, password = ? WHERE id = ?;", user["name"], user["mail"], user['admin'], sha256_crypt.hash(user["pwd"]), _id)
                else:
                    cursor.execute("UPDATE users SET name = ?, mail = ?, admin = ? WHERE id = ?;", user["name"], user["mail"], user['admin'], _id)
                connection.commit()

                return jsonify({'message': 'OK'}), 200
            return jsonify({'message': 'User Doesn\'t Exists'}), 401
        except:
            return jsonify({'message': 'Unknown Error'}), 400
        finally:
            if connection is not None:
                close(connection)

    return jsonify({'message': 'Wrong Format'}), 400


@users_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    body = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(body), 200 
    

def fetch_all_users(cursor):
    dictionary = {}
    row = cursor.fetchone()
    count = 0

    while row:
        dictionary[count] = {"id": row[0], 'name': row[1], 'mail': row[2], 'admin': row[3]}
        row = cursor.fetchone()
        count += 1

    return dictionary


def check_if_user_exists_by_id(cursor, _id):
    return True if cursor.execute("SELECT COUNT(id) FROM users WHERE id = ?", _id).fetchone()[0] == 1 else False


def check_if_user_exists_by_mail(cursor, mail):
    return True if cursor.execute("SELECT COUNT(mail) FROM users WHERE mail = ?", mail).fetchone()[0] == 1 else False
