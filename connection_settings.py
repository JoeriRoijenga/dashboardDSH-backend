import pyodbc


driver = "{ODBC Driver 17 for SQL Server}"
server = "tcp:iot-db-roijenga.database.windows.net,1433"
database = "iot-db-weather-pi"
username = "iot-joeri-roijenga"
password = "cO1WfBYif7eA"
encryption = "yes"
certificate = "no"
timeout = "30"

connection_string = 'Driver=%s;Server=%s;Database=%s;Uid=%s;Pwd=%s;Encrypt=%s;TrustServerCertificate=%s;Connection Timeout=%s;' % (
    driver, server, database, username, password, encryption, certificate, timeout)


def connect():
    conn = pyodbc.connect(connection_string)
    curs = conn.cursor()
    return conn, curs


def close(conn):
    conn.close()