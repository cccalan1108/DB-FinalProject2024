import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from Action import Action
from flask import request, jsonify, Blueprint
from DB_utils import DatabaseManager as db_manager

login = Blueprint("login", __name__)

class LoginAction(Action):
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cur = db_manager
        
    def exec(self):
        # 讀取帳號密碼
        account = request.form.get('account')  # 從 POST 請求中獲取帳號
        password = request.form.get('password')  # 從 POST 請求中獲取密碼
        
        cmd = """
            select u.account, u.password
            from user as u
            where u.account = %s and u.password = %s
            """
        
        # 執行查詢
        self.cur.execute(cmd, [account, password])
        users = self.cur.fetchall()

        if len(users) != 1:
            # 登入失敗
            response = {
                "status": "error",
                "message": "Invalid account or password!"
            }
            return jsonify(response)
        else:
            # 根據角色生成回應
            response = {
                "status": "success",
                "message": f"Welcome back, {users[0]['user_name']}!",
                "user_id": users[0]["user_id"],
                "role": users[0]["role"]
            }
            return jsonify(response)

login_action = LoginAction(db_manager = None)

@login.route('/submit-login', methods=['POST'])
def login_route():
    return login_action.exec()