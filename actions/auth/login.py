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
        self.db_manager = db_manager
        
    def exec(self):
        # 讀取帳號密碼
        account = request.form.get('account')  # 從 POST 請求中獲取帳號
        password = request.form.get('password')  # 從 POST 請求中獲取密碼
        
        self.db_manager.verify_login(account, password)

login_action = LoginAction(db_manager)

@login.route('/submit-login', methods=['POST'])
def login_route():
    return login_action.exec()