INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Temperature');
INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Humidity');
INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Pressure');

INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (1, 'notifications', 1);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (1, 'sms', 0);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (1, 'mail', 1);

INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (2, 'notifications', 1);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (2, 'sms', 0);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (2, 'mail', 1);

INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (3, 'notifications', 1);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (3, 'sms', 0);
INSERT INTO [dbo].[sensor_types_settings] ("sensor_types_id", "type", "on") VALUES (3, 'mail', 1);

INSERT INTO [dbo].[general_settings] ("type", "on") VALUES ('notifications', 1);
INSERT INTO [dbo].[general_settings] ("type", "on") VALUES ('sms', 1);
INSERT INTO [dbo].[general_settings] ("type", "on") VALUES ('mail', 1);

INSERT INTO [dbo].[sensors] ("name", "sensor_types_id") VALUES ('temp1', 1);

INSERT INTO [dbo].[actuator_types] ("name", "type") VALUES ('Ventilator', 'BOOLEAN');
INSERT INTO [dbo].[actuator_types] ("name", "type") VALUES ('Door', 'INT');
INSERT INTO [dbo].[actuator_types] ("name", "type") VALUES ('Window', 'INT');

INSERT INTO [dbo].[actuators] ("name", "actuator_types_id", "current_state") VALUES ('Vent', 1, 1);
INSERT INTO [dbo].[actuators] ("name", "actuator_types_id", "current_state") VALUES ('Door1', 2, 10);
INSERT INTO [dbo].[actuators] ("name", "actuator_types_id", "current_state") VALUES ('Window1', 3, 20);