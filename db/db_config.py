import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="containers-us-west-17.railway.app",
        user="root",
        password="zSZTEQIkTIvckSAbxaqiIMqphRyuUfzs",
        database="railway",
        port=17843,
        unix_socket=None
    )
