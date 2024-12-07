import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from Action import Action
from datetime import datetime
from DB_utils import DatabaseManager as db_manager
from flask import request, jsonify, Blueprint


signUp = Blueprint("signUp", __name__)

class SignUpAction(Action):
    def __init__(self, db_manager):
        if not db_manager:
            raise ValueError("DatabaseManager instance is required")
        self.db_manager = db_manager

    def exec(self):
        try:
            account = request.form.get('account')
            # 確認帳號是否存在
            if self.db_manager and self.db_manager.check_account_exists(account):
                response = {
                    "status": "error",
                    "message": "Account already exists!",
                }
                return jsonify(response)

            password = request.form.get('password')          
            user_name = request.form.get('name')           
            user_nickname = request.form.get('nickname')                
            nationality = request.form.get('nationality')
            phone = request.form.get('phone')             
            email = request.form.get('email')         
            sex = request.form.get('gender')
            birthday = request.form.get('birthday')
            city = request.form.get('city')
            admin_code = request.form.get('admin_code')

            if self.db_manager:
                success = self.db_manager.create_user(
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
                    register_time=datetime.now(),
                    admin_code = admin_code
                )
                
                if success:
                    response = {
                        "status": "success",
                        "message": "Registration successful!\nYou can now log in and add more personal details in your profile."
                    }
                    return jsonify(response)
                else:
                    response = {
                        "status": "error",
                        "message": "Registration failed!"
                    }
                    return jsonify(response)
            
            return jsonify({"status": "error", "message": "ERROR"})
            
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error in signup: {e}"
            }
            return jsonify(response)
        
signUp_action = SignUpAction(db_manager)

@signUp.route('/submit-register', methods=['POST'])
def signUp_route():
    return signUp_action.exec()



# from ..Action import Action
# from datetime import datetime

# class SignUpAction(Action):
#     ADMIN_AUTH_CODE = "belloadmin"
    
#     def __init__(self):
#         super().__init__("Sign Up")
        
#     def exec(self, conn, db_manager=None):
#         try:
#             self.send_message(conn, "\n=== User Registration ===")
#             self.send_message(conn, "* indicates required field")
            
#             # necessary information
#             account = self.read_input(conn, "*Account (max 15 characters)")
#             while len(account) > 15 or len(account) == 0:
#                 self.send_message(conn, "Account length must be between 1 and 15 characters")
#                 account = self.read_input(conn, "*Account (max 15 characters)")
                
#             password = self.read_input(conn, "*Password (max 15 characters)")
#             while len(password) > 15 or len(password) == 0:
#                 self.send_message(conn, "Password length must be between 1 and 15 characters")
#                 password = self.read_input(conn, "*Password (max 15 characters)")
                
#             user_name = self.read_input(conn, "*Real name (max 20 characters)")
#             while len(user_name) > 20 or len(user_name) == 0:
#                 self.send_message(conn, "Name length must be between 1 and 20 characters")
#                 user_name = self.read_input(conn, "*Real name (max 20 characters)")
                
#             user_nickname = self.read_input(conn, "*Nickname (max 20 characters)")
#             while len(user_nickname) > 20 or len(user_nickname) == 0:
#                 self.send_message(conn, "Nickname length must be between 1 and 20 characters")
#                 user_nickname = self.read_input(conn, "*Nickname (max 20 characters)")
                
#             nationality = self.read_input(conn, "*Nationality (max 20 characters)")
#             while len(nationality) > 20 or len(nationality) == 0:
#                 self.send_message(conn, "Nationality must be between 1 and 20 characters")
#                 nationality = self.read_input(conn, "*Nationality (max 20 characters)")
            
#             phone = self.read_input(conn, "*Phone number (max 20 characters)")
#             while len(phone) > 20 or len(phone) == 0:
#                 self.send_message(conn, "Phone number must be between 1 and 20 characters")
#                 phone = self.read_input(conn, "*Phone number (max 20 characters)")
                
#             email = self.read_input(conn, "*Email (max 50 characters)")
#             while len(email) > 50 or len(email) == 0:
#                 self.send_message(conn, "Email must be between 1 and 50 characters")
#                 email = self.read_input(conn, "*Email (max 50 characters)")
            
#             sex = self.read_input(conn, "*Gender (M/F)")
#             while sex.upper() not in ['M', 'F']:
#                 self.send_message(conn, "Please enter M or F")
#                 sex = self.read_input(conn, "*Gender (M/F)")
                
#             birthday = self.read_input(conn, "*Birthday (YYYY-MM-DD)")
            
#             # Optional information
#             city = self.read_input(conn, "City (max 20 characters)")
#             if city and len(city) > 20:
#                 self.send_message(conn, "City name too long, will be truncated to 20 characters")
#                 city = city[:20]
            
#             auth_code = self.read_input(conn, "Enter admin authorization code (enter 'none' to skip)")
#             is_admin = False
#             if auth_code.lower() != 'none':
#                 is_admin = (auth_code == self.ADMIN_AUTH_CODE)
            
#             if db_manager and db_manager.check_account_exists(account):
#                 self.send_message(conn, "Account already exists!")
#                 return False
                
#             if db_manager:
#                 success = db_manager.create_user(
#                     account=account,
#                     password=password,
#                     user_name=user_name,
#                     user_nickname=user_nickname,
#                     nationality=nationality,
#                     city=city,
#                     phone=phone,
#                     email=email,
#                     sex=sex,
#                     birthday=birthday,
#                     register_time=datetime.now(),
#                     is_admin=is_admin
#                 )
                
#                 if success:
#                     role = "Admin" if is_admin else "User"
#                     self.send_message(conn, f"Registration successful! Role: {role}")
#                     return True
#                 else:
#                     self.send_message(conn, "Registration failed!")
#                     return False
            
#             return False
            
#         except Exception as e:
#             print(f"Error in signup: {e}")
#             self.send_message(conn, "Registration failed due to an error")
#             return False