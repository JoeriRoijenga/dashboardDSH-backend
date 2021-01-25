import pyodbc

driver = "{ODBC Driver 17 for SQL Server}"
server = "tcp:iot-server-ruimte.database.windows.net,1433"
database = "dbo"
username = "iot-joeri-roijenga"
password = "cO1WfBYif7eA"
encryption = "yes"
certificate = "no"
timeout = "30"

connection_string = 'Driver=%s;Server=%s;Database=%s;Uid=%s;Pwd=%s;Encrypt=%s;TrustServerCertificate=%s;Connection Timeout=%s;' % (
    driver, server, database, username, password, encryption, certificate, timeout)

# "Driver={ODBC Driver 13 for SQL Server};Server=tcp:iot-server-ruimte.database.windows.net,1433;Database=dbo;Uid=iot-joeri-roijenga;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def connect():
    conn = pyodbc.connect(connection_string)
    curs = conn.cursor()
    return conn, curs


def close(conn):
    conn.close()
