IF EXISTS(SELECT 1 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.sensor_data'))
  ALTER TABLE dbo.sensor_data DROP CONSTRAINT fk_sensor_data_sensors1;

IF EXISTS(SELECT 1 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.actuators'))
  ALTER TABLE dbo.actuators DROP CONSTRAINT fk_actuators_actuator_types1;  

IF EXISTS(SELECT 1 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.sensors'))
  ALTER TABLE dbo.sensors DROP CONSTRAINT fk_sensors_sensor_types1;  

IF EXISTS(SELECT 2 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.rules'))  
  ALTER TABLE dbo.rules DROP CONSTRAINT fk_sensors_has_actuators_sensors;

IF EXISTS(SELECT 1 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.rules'))
  ALTER TABLE dbo.rules DROP CONSTRAINT fk_sensors_has_actuators_actuators1;  
  
IF EXISTS(SELECT 1 FROM sys.foreign_keys WHERE parent_object_id = OBJECT_ID(N'dbo.sensor_settings'))
  ALTER TABLE dbo.sensor_settings DROP CONSTRAINT fk_sensor_settings_sensors1;  


IF OBJECT_ID('dbo.users', 'u') IS NOT NULL 
  DROP TABLE dbo.users;

IF OBJECT_ID('dbo.rules', 'u') IS NOT NULL 
  DROP TABLE dbo.rules;

IF OBJECT_ID('dbo.sensors', 'u') IS NOT NULL 
  DROP TABLE dbo.sensors;

IF OBJECT_ID('dbo.sensor_types', 'u') IS NOT NULL 
  DROP TABLE dbo.sensor_types;

IF OBJECT_ID('dbo.actuators', 'u') IS NOT NULL 
  DROP TABLE dbo.actuators;

IF OBJECT_ID('dbo.actuator_types', 'u') IS NOT NULL 
  DROP TABLE dbo.actuator_types;

IF OBJECT_ID('dbo.sensor_data', 'u') IS NOT NULL 
  DROP TABLE dbo.sensor_data;

IF OBJECT_ID('dbo.general_settings', 'u') IS NOT NULL 
  DROP TABLE dbo.general_settings;

IF OBJECT_ID('dbo.sensor_settings', 'u') IS NOT NULL 
  DROP TABLE dbo.sensor_settings;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo`.`users`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.users (
  [id] INT NOT NULL IDENTITY,
  [mail] VARCHAR(45) NOT NULL,
  [name] VARCHAR(45) NOT NULL,
  [password] VARCHAR(100) NOT NULL,
  [admin] SMALLINT NOT NULL,
  PRIMARY KEY ([id]))
;

-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.sensor_types`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.sensor_types (
  [id] INT NOT NULL IDENTITY,
  [name] VARCHAR(45) NOT NULL,
  PRIMARY KEY ([id]))
;

-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.sensors`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.sensors (
  [id] INT NOT NULL IDENTITY,
  [name] VARCHAR(45) NOT NULL,
  [sensor_types_id] INT NOT NULL,
  PRIMARY KEY ([id])
  ,
  CONSTRAINT [fk_sensors_sensor_types1]
    FOREIGN KEY ([sensor_types_id])
    REFERENCES dbo.sensor_types ([id])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.sensor_data`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.sensor_data (
  [id] INT NOT NULL IDENTITY,
  [sensors_id] INT NOT NULL,
  [datetime] VARCHAR(45) NOT NULL,
  [value] VARCHAR(45) NOT NULL,
  PRIMARY KEY ([id], [sensors_id], [datetime])
 ,
  CONSTRAINT [fk_sensor_data_sensors1]
    FOREIGN KEY ([sensors_id])
    REFERENCES dbo.sensors ([id]))
;

CREATE INDEX [fk_sensor_data_sensors1_idx] ON dbo.sensor_data ([sensors_id] ASC)


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.actuator_types`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.actuator_types (
  [id] INT NOT NULL IDENTITY,
  [name] VARCHAR(45) NOT NULL,
  [type] VARCHAR(45) NOT NULL,
  PRIMARY KEY ([id]))
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.actuators`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.actuators (
  [id] INT NOT NULL IDENTITY,
  [name] VARCHAR(45) NOT NULL,
  [actuator_types_id] INT NOT NULL,
  [current_state] INT NULL DEFAULT NULL,
  PRIMARY KEY ([id])
 ,
  CONSTRAINT [fk_actuators_actuator_types1]
    FOREIGN KEY ([actuator_types_id])
    REFERENCES dbo.actuator_types ([id])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX [fk_actuators_actuator_types1_idx] ON dbo.actuators ([actuator_types_id] ASC);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** Table `dbo`.`rules`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.rules (
  [sensors_id] INT NOT NULL,
  [actuators_id] INT NOT NULL,
  [type] VARCHAR(45) NOT NULL,
  [value] INT NOT NULL,
  [respond_value] INT NOT NULL,
  PRIMARY KEY ([sensors_id], [actuators_id])
 ,
  CONSTRAINT [fk_sensors_has_actuators_sensors]
    FOREIGN KEY ([sensors_id])
    REFERENCES dbo.sensors ([id])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT [fk_sensors_has_actuators_actuators1]
    FOREIGN KEY ([actuators_id])
    REFERENCES dbo.actuators ([id])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX [fk_sensors_has_actuators_actuators1_idx] ON dbo.rules ([actuators_id] ASC);
CREATE INDEX [fk_sensors_has_actuators_sensors_idx] ON dbo.rules ([sensors_id] ASC);


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.general_settings`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.general_settings (
  [id] INT NOT NULL IDENTITY,
  [type] VARCHAR(45) NOT NULL,
  [on] SMALLINT NOT NULL,
  PRIMARY KEY ([id]))
;


-- SQLINES DEMO *** ------------------------------------
-- SQLINES DEMO *** `dbo.sensor_settings`
-- SQLINES DEMO *** ------------------------------------
CREATE TABLE dbo.sensor_settings (
  [id] INT NOT NULL IDENTITY,
  [sensors_id] INT NOT NULL,
  [type] VARCHAR(45) NOT NULL,
  [value] INT NOT NULL,
  [on] SMALLINT NOT NULL,
  PRIMARY KEY ([id], [sensors_id], [type])
 ,
  CONSTRAINT [fk_sensor_settings_sensors1]
    FOREIGN KEY ([sensors_id])
    REFERENCES dbo.sensors ([id])
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
;

CREATE INDEX [fk_sensor_settings_sensors1_idx] ON dbo.sensor_settings ([sensors_id] ASC);


