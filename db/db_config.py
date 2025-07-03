import mysql.connector

def get_connection():
    host = "sql12.freesqldatabase.com"
    port = 3306
    user = "sql12787920"
    password = "wfcdEp3R45"
    database = "sql12787920"

    # Debug print
    print("[DB DEBUG] host:", host)
    print("[DB DEBUG] port:", port)
    print("[DB DEBUG] user:", user)
    print("[DB DEBUG] password:", "(hidden for safety)")
    print("[DB DEBUG] database:", database)

    # Just in case: sanity check
    if not all([host, port, user, password, database]):
        raise ValueError("One or more DB credentials are missing")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
