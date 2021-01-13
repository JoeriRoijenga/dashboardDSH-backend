INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Temperature');
INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Humidity');
INSERT INTO [dbo].[sensor_types] ("name") VALUES ('Pressure');

INSERT INTO [dbo].[sensors] ("name", "sensor_types_id") VALUES ('temp1', 1);