import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

def get_db_cursor(db_name):
    postgresql_conn = psycopg2.connect(user = "dbuser", password = "guest", host = "localhost", port = "5432", database = db_name)
    postgresql_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return postgresql_conn.cursor()

cursor = get_db_cursor("postgres")
cursor.execute("DROP DATABASE IF EXISTS search_db;")
cursor.execute("CREATE DATABASE search_db;")

