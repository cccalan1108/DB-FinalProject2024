import psycopg2
import os
from dotenv import load_dotenv


# global psql connection instance
conn = None

def init_db_conn():
    load_dotenv()  # load env file info of database login
    DB_USER_NAME     = os.getenv('DB_USER_NAME')
    DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
    DB_ADDRESS       = os.getenv('DB_ADDRESS')
    DB_NAME          = os.getenv('DB_NAME')
    
    conn = psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER_NAME,
        host = DB_ADDRESS,
        password = DB_USER_PASSWORD
    )
