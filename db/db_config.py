import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="containers-us-west-17.railway.app",  # ✅ this is the PUBLIC HOSTNAME
        user="root",
        password="zSZTEQIkTIvckSAbxaqiIMqphRyuUfzs",
        database="railway",
        port=3306,  # or the actual Railway public port if shown
        unix_socket=None
    )