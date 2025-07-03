from dotenv import load_dotenv
load_dotenv()

import os
import mysql.connector

def get_connection():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if not all([host, port, user, password, database]):
        raise ValueError("One or more DB environment variables are missing")

    return mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database
    )
