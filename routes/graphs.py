from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close

graphs_bp = Blueprint("graphs", __name__)

@graphs_bp.route('/get/sensor/data', methods=["GET"])
@jwt_required
def get_sensor_data():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT sensor_id, datetime, value FROM sensor_data;")
        
        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "datetime": row[1], "value": row[2]})
            row = cursor.fetchone()

        return jsonify({'sensor_data': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)