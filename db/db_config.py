import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",         # <-- replace with actual host
        port=3306,                               # usually 3306
        user="sql12787920",                      # your DB username
        password="wfcdEp3R45",             # your DB password
        database="sql12787920",
        connect_timeout=10,
        use_pure=True# your DB name
    )

