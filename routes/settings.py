from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close

settings_bp = Blueprint("settings", __name__)

@settings_bp.route('/get/general', methods=["GET"])
@jwt_required
def get_general_settings():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT \"type\", \"on\" FROM general_settings;")
        
        returnData = []
        row = cursor.fetchone()
        count = 0

        while row:
            returnData.append({"type": row[0], "on": row[1]})
            row = cursor.fetchone()
            count += 1

        return jsonify({'settings': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)

@settings_bp.route('/save/general', methods=["PUT"])
@jwt_required
def save_general_settings():
    if (request.is_json):
        settings = request.get_json()["settings"]
        print(settings)
        try:
            connection, cursor = connect()
            # for item in settings:
                # print(item["type"] + " : " + item["on"])
            # cursor.execute("UPDATE general_settings SET \"type\" = '?', \"on\" = '?';", settings[])
            return jsonify({'message': "success"}), 200
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            close(connection)