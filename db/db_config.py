import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="mysql-xl07.railway.internal",
        user="root",
        password="zSZTEQIkTIvckSAbxaqiIMqphRyuUfzs",
        database="railway",
        port=3306,
        unix_socket=None
    )
