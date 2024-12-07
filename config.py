from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Database settings
    DB_NAME = os.getenv('DB_NAME', 'bello')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '0000')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5430')

    # Server settings
    SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
    SERVER_PORT = int(os.getenv('SERVER_PORT', '8800'))