from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close

graphs_bp = Blueprint("graphs", __name__)

@graphs_bp.route('/get/sensor/data', methods=["POST"])
@jwt_required
def get_sensor_data():
    connection = None

    try:
        connection, cursor = connect()
        
        if request.is_json:
            data = request.get_json()
            if (len(data) != 1):
                cursor.execute("SELECT \"sensors_id\", \"datetime\", \"value\" FROM sensor_data WHERE \"datetime\" > ? AND \"sensors_id\" = ?;", data["datetime"],  data["id"])
            else:
                cursor.execute("SELECT \"sensors_id\", \"datetime\", \"value\" FROM sensor_data WHERE \"sensors_id\" = ?;", data["id"])
            
            returnData = []
            
            row = cursor.fetchone()

            while row:
                returnData.append({"id": row[0], "datetime": row[1], "value": row[2]})
                row = cursor.fetchone()

            return jsonify({'sensor_data': returnData}), 200
        return jsonify({'error': "Wrong format JSON"}), 400
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)


@graphs_bp.route('/get/sensors', methods=["GET"])
@jwt_required
def get_sensors():
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("SELECT sensors.id, sensors.name, sensor_types.name FROM sensors JOIN sensor_types ON sensors.sensor_types_id = sensor_types.id;")
        
        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "name": row[1], "type": row[2]})
            row = cursor.fetchone()

        return jsonify({'sensors': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)