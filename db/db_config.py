import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=os.getenv("MYSQLPORT"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )
