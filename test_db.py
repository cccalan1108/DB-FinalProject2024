from DB_utils import DatabaseManager

def test_connection():
    db = DatabaseManager()
    if db.connect():
        print("Test connection successful")
        db.close()
    else:
        print("Test connection failed")

if __name__ == "__main__":
    test_connection()