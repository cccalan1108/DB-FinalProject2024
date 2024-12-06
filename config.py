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


##Test
print("=== Environment Variables ===")
print(f"DB_NAME: {Config.DB_NAME}")
print(f"DB_USER: {Config.DB_USER}")
print(f"DB_PASSWORD: {Config.DB_PASSWORD}")
print(f"DB_HOST: {Config.DB_HOST}")
print(f"DB_PORT: {Config.DB_PORT}")
print(f"SERVER_HOST: {Config.SERVER_HOST}")
print(f"SERVER_PORT: {Config.SERVER_PORT}")
print("==========================")