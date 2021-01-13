from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close
import json

settings_bp = Blueprint("settings", __name__)

@settings_bp.route('/get/general', methods=["GET"])
@jwt_required
def get_general_settings():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT \"type\", \"on\" FROM general_settings;")
        
        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"type": row[0], "on": row[1]})
            row = cursor.fetchone()

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
        try:
            connection, cursor = connect()
    
            for key in settings.keys():
                cursor.execute("UPDATE general_settings SET \"on\" = ? WHERE \"type\" = ?;", str(settings[key]), str(key))
    
            connection.commit()
            return jsonify({'message': "success"}), 200
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            close(connection)


@settings_bp.route('/get/sensors/<string:_id>', methods=["GET"])
@jwt_required
def get_sensors(_id):
    try:
        connection, cursor = connect()

        cursor.execute("SELECT sensors.id, sensors.name, sensor_types.name FROM sensors JOIN sensor_types ON sensors.sensor_types_id = sensor_types.id WHERE sensors.sensor_types_id = ?;", _id)
        
        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "name": row[1], "type": row[2]})
            row = cursor.fetchone()

        return jsonify({'sensors': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)


@settings_bp.route('/get/sensor/types', methods=["GET"])
@jwt_required
def get_sensor_types():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT * FROM sensor_types;")

        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "name": row[1]})
            row = cursor.fetchone()

        return jsonify({'sensor_types': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)


@settings_bp.route('/get/sensor/type/notifications/<string:_id>', methods=["GET"])
@jwt_required
def get_sensor_type_notifications(_id):
    try:
        connection, cursor = connect()

        cursor.execute("SELECT \"type\", \"on\" FROM sensor_types_settings WHERE sensor_types_id = ?;", _id)

        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"type": row[0], "on": row[1]})
            row = cursor.fetchone()

        return jsonify({'notification_settings': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)


@settings_bp.route('/save/sensor/type/notifications/<string:_id>', methods=["PUT"])
@jwt_required
def save_sensor_type_notifications(_id):
    if (request.is_json):
        settings = request.get_json()["settings"]
        try:
            connection, cursor = connect()
    
            for key in settings.keys():
                cursor.execute("UPDATE sensor_types_settings SET \"on\" = ? WHERE \"type\" = ? AND \"sensor_types_id\" = ?;", str(settings[key]), str(key), _id)
    
            connection.commit()
            return jsonify({'message': "success"}), 200
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            close(connection)

@settings_bp.route('/get/actuators', methods=["GET"])
@jwt_required
def get_actuators():
    try:
        connection, cursor = connect()

        cursor.execute("SELECT actuators.id, actuators.name, actuators.current_state, actuator_types.name, actuator_types.type FROM actuators JOIN actuator_types ON actuators.actuator_types_id = actuator_types.id")
        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "name": row[1], "current_state": row[2], "type_name": row[3], "type": row[4]})
            row = cursor.fetchone()

        return jsonify({'actuators': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        close(connection)
