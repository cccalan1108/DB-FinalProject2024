from .action import Action
from role.user import User
from role.admin import Admin
from DB_utils import db

class LogIn(Action):
    def exec(self, conn):
        userid = self.read_input(conn, "userid")
        print(f'Read userid: {userid}')

        while not userid.isdigit():
            conn.send("Input is not numeric, ".encode('utf-8'))
            userid = self.read_input(conn, "correct userid")


        username, pwd, email, isUser, isAdmin = fetch_user(userid)
        print(f'--After fetch')

        while username is None:
            conn.send("Userid not exist, ".encode('utf-8'))
            userid = self.read_input(conn, "correct userid")
            username, pwd, email, isUser, isAdmin = fetch_user(userid)

        pwd_input = self.read_input(conn, "password")
        print(f'Read pwd: {pwd_input}')
        count = 2
        
        while count > 0 and pwd_input != pwd:
            conn.send(f'[INPUT]Password incorrect, please enter password (remaining try: {count}): '.encode('utf-8'))
            pwd_input = conn.recv(100).decode("utf-8")
            count -= 1
        if count == 0:
            conn.send(f'[EXIT]Connection close. Reason: Password incorrect.'.encode('utf-8'))
            return -1
        
        if isAdmin:
            return Admin(userid, username, pwd, email)
            
        else:
            return User(userid, username, pwd, email)


#new
from flask import Flask, request, jsonify, Blueprint
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

@login.route('/login', methods=['POST'])
def login_route():
    return login_action.exec()