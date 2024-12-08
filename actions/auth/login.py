import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from Action import Action
from flask import request, Blueprint
from DB_utils import DatabaseManager as db_manager

login = Blueprint("login", __name__)

class LoginAction(Action):
    def __init__(self, db_manager):
        self.db_manager = db_manager()
        
    def exec(self):
        # 讀取帳號密碼
        account = request.form.get('account')  # 從 POST 請求中獲取帳號
        password = request.form.get('password')  # 從 POST 請求中獲取密碼
        print(account,password)
        print("DEBUG: self.db_manager type:", type(self.db_manager))
        return self.db_manager.verify_login(account, password)

login_action = LoginAction(db_manager)

@login.route('/submit-login', methods=['POST'])
def login_route():
    return login_action.exec()



# from ..Action import Action
# from role.User import User
# from role.Admin import Admin

# class LoginAction(Action):
#     def __init__(self):
#         super().__init__("Login")
        
#     def exec(self, conn, db_manager=None):
#         account = self.read_input(conn, "Enter your account")
#         password = self.read_input(conn, "Enter your password")
        
#         result = db_manager.verify_login(account, password) 
#         if result:
#             self.send_message(conn, f"\nWelcome back, {result['user_name']}!")
#             self.send_message(conn, f"Your ID is: {result['user_id']}")
            
#             if result['role'] == 'Admin':
#                 user = Admin(result['user_id'], result['user_name'], 
#                            password, result['email'])
#             else:
#                 user = User(result['user_id'], result['user_name'], 
#                           password, result['email'])
#             return user
        
#         self.send_message(conn, "Invalid account or password!")
#         return None
        