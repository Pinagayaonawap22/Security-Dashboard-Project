import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "mysql-xl07.railway.internal"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE", "railway")
    )