from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close

settings_bp = Blueprint("settings", __name__)

@settings_bp.route('/get/general', methods=["GET"])
@jwt_required
def get_general_settings():
    connection, cursor = connect()

    try:
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