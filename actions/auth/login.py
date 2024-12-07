from actions import Action
from DB_utils import db

#new
from flask import request, jsonify, Blueprint
from DB_utils import db

login = Blueprint("login", __name__)

class LoginAction(Action):
    cur = None

    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def exec(self):
        cur = db.cursor()

        # 讀取帳號密碼
        account = request.form.get('account')  # 從 POST 請求中獲取帳號
        password = request.form.get('password')  # 從 POST 請求中獲取密碼
        
        cmd = """
            select u.account, u.password
            from user as u
            where u.account = %s and u.password = %s
            """
        
        # 執行查詢
        cur.execute(cmd, [account, password])
        users = cur.fetchall()

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