from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from connection_settings import connect, close

settings_bp = Blueprint("settings", __name__)

@settings_bp.route('/get/general', methods=["GET"])
@jwt_required
def get_general_settings():
    connection = None

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
        if connection is not None:
            close(connection)

@settings_bp.route('/save/general', methods=["PUT"])
@jwt_required
def save_general_settings():
    connection = None

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
            if connection is not None:
                close(connection)


@settings_bp.route('/get/sensors/<string:_id>', methods=["GET"])
@jwt_required
def get_sensors(_id):
    connection = None

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
        if connection is not None:
            close(connection)


@settings_bp.route('/get/sensors', methods=["GET"])
@jwt_required
def get_all_sensors():
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("SELECT * FROM sensors;")
        
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


@settings_bp.route('/get/sensor/types', methods=["GET"])
@jwt_required
def get_sensor_types():
    connection = None

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
        if connection is not None:
            close(connection)


@settings_bp.route('/get/sensor/type/notifications/<string:_id>', methods=["GET"])
@jwt_required
def get_sensor_type_notifications(_id):
    connection = None

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
        if connection is not None:
            close(connection)


@settings_bp.route('/save/sensor/type/notifications/<string:_id>', methods=["PUT"])
@jwt_required
def save_sensor_type_notifications(_id):
    connection = None

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
            if connection is not None:
                close(connection)


@settings_bp.route('/get/actuators', methods=["GET"])
@jwt_required
def get_actuators():
    connection = None

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
        if connection is not None:
            close(connection)


@settings_bp.route('/get/rule/<string:_id>', methods=["GET"])
@jwt_required
def get_rule(_id):
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("SELECT id, value, type, respond_value, actuators_id, sensors_id FROM rules WHERE rules.id = ?;", _id)

        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "sensor_id": row[5], "actuator_id": row[4], "type": row[2], "value": row[1], "respond_value": row[3]})
            row = cursor.fetchone()

        return jsonify({'rule': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)


@settings_bp.route('/get/rules', methods=["GET"])
@jwt_required
def get_rules():
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("SELECT rules.id, rules.value, rules.type, respond_value, sensors.name, actuators.name FROM rules JOIN actuators ON actuators.id = rules.actuators_id JOIN sensors ON sensors.id = rules.sensors_id")

        returnData = []
        row = cursor.fetchone()

        while row:
            returnData.append({"id": row[0], "sensor_name": row[4], "actuator_name": row[5], "type": row[2], "value": row[1], "respond_value": row[3]})
            row = cursor.fetchone()

        return jsonify({'rules': returnData}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)


@settings_bp.route('/add/rules', methods=["POST"])
@jwt_required
def add_rules():
    connection = None

    if (request.is_json):
        rules = request.get_json()
        print(rules)
        try:
            connection, cursor = connect()
    
            cursor.execute("INSERT INTO rules ( \"sensors_id\", \"actuators_id\", \"type\", \"value\", \"respond_value\") VALUES (?, ?, ?, ?, ?);", rules['sensors_id'], rules['actuators_id'], rules['type'], rules['value'], rules['respond_value'])
            connection.commit()

            return jsonify({'message': "success"}), 200
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            if connection is not None:
                close(connection)


@settings_bp.route('/edit/rules/<string:_id>', methods=["PUT"])
@jwt_required
def edit_rules(_id):
    connection = None

    if (request.is_json):
        rules = request.get_json()

        try:
            connection, cursor = connect()
    
            cursor.execute("UPDATE rules SET \"sensors_id\" = ?, \"actuators_id\" = ?, \"type\" = ?, \"value\" = ?, \"respond_value\" = ? WHERE \"id\" = ?;", rules['sensors_id'], rules['actuators_id'], rules['type'], rules['value'], rules['respond_value'], _id)
            connection.commit()
            
            return jsonify({'message': "success"}), 200
        except:
            return jsonify({'error': 'Unknown Error'}), 400
        finally:
            if connection is not None:
                close(connection)


@settings_bp.route('/delete/rules/<string:_id>', methods=["DELETE"])
@jwt_required
def delete_rules(_id):
    connection = None

    try:
        connection, cursor = connect()

        cursor.execute("DELETE FROM rules WHERE \"id\" = ?;", _id)
        connection.commit()
        
        return jsonify({'message': "success"}), 200
    except:
        return jsonify({'error': 'Unknown Error'}), 400
    finally:
        if connection is not None:
            close(connection)