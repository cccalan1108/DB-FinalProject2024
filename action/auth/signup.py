from ..Action import Action
from datetime import datetime

class SignUpAction(Action):
    def __init__(self):
        super().__init__("Sign Up")
        
    def exec(self, conn, db_manager=None):
        try:
            self.send_message(conn, "\n=== User Registration ===")
            self.send_message(conn, "* indicates required field")
            
            # necessary information
            account = self.read_input(conn, "*Account (max 15 characters)")
            while len(account) > 15 or len(account) == 0:
                self.send_message(conn, "Account length must be between 1 and 15 characters")
                account = self.read_input(conn, "*Account (max 15 characters)")
                
            password = self.read_input(conn, "*Password (max 15 characters)")
            while len(password) > 15 or len(password) == 0:
                self.send_message(conn, "Password length must be between 1 and 15 characters")
                password = self.read_input(conn, "*Password (max 15 characters)")
                
            user_name = self.read_input(conn, "*Real name (max 20 characters)")
            while len(user_name) > 20 or len(user_name) == 0:
                self.send_message(conn, "Name length must be between 1 and 20 characters")
                user_name = self.read_input(conn, "*Real name (max 20 characters)")
                
            user_nickname = self.read_input(conn, "*Nickname (max 20 characters)")
            while len(user_nickname) > 20 or len(user_nickname) == 0:
                self.send_message(conn, "Nickname length must be between 1 and 20 characters")
                user_nickname = self.read_input(conn, "*Nickname (max 20 characters)")
                
            nationality = self.read_input(conn, "*Nationality (max 20 characters)")
            while len(nationality) > 20 or len(nationality) == 0:
                self.send_message(conn, "Nationality must be between 1 and 20 characters")
                nationality = self.read_input(conn, "*Nationality (max 20 characters)")
            
            phone = self.read_input(conn, "*Phone number (max 20 characters)")
            while len(phone) > 20 or len(phone) == 0:
                self.send_message(conn, "Phone number must be between 1 and 20 characters")
                phone = self.read_input(conn, "*Phone number (max 20 characters)")
                
            email = self.read_input(conn, "*Email (max 50 characters)")
            while len(email) > 50 or len(email) == 0:
                self.send_message(conn, "Email must be between 1 and 50 characters")
                email = self.read_input(conn, "*Email (max 50 characters)")
            
            sex = self.read_input(conn, "*Gender (M/F)")
            while sex.upper() not in ['M', 'F']:
                self.send_message(conn, "Please enter M or F")
                sex = self.read_input(conn, "*Gender (M/F)")
                
            birthday = self.read_input(conn, "*Birthday (YYYY-MM-DD)")
            
            # Optional information
            city = self.read_input(conn, "City (max 20 characters)")
            if city and len(city) > 20:
                self.send_message(conn, "City name too long, will be truncated to 20 characters")
                city = city[:20]
            
            if db_manager and db_manager.check_account_exists(account):
                self.send_message(conn, "Account already exists!")
                return False
                
            if db_manager:
                success = db_manager.create_user(
                    account=account,
                    password=password,
                    user_name=user_name,
                    user_nickname=user_nickname,
                    nationality=nationality,
                    city=city,
                    phone=phone,
                    email=email,
                    sex=sex,
                    birthday=birthday,
                    register_time=datetime.now()
                )
                
                if success:
                    self.send_message(conn, "Registration successful!")
                    self.send_message(conn, "You can now log in and add more personal details in your profile.")
                    return True
                else:
                    self.send_message(conn, "Registration failed!")
                    return False
            
            return False
            
        except Exception as e:
            print(f"Error in signup: {e}")
            self.send_message(conn, "Registration failed due to an error")
            return False