import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host     = os.getenv("MYSQLHOST"),
        user     = os.getenv("MYSQLUSER"),
        password = os.getenv("MYSQLPASSWORD"),
        database = os.getenv("MYSQLDATABASE"),
        port     = int(os.getenv("MYSQLPORT", 3306))
    )
