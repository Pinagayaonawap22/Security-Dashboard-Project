import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASS"),
        database=os.getenv("MYSQLDB"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )
