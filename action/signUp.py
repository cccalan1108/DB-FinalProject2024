
from .action import Action
from role.user import User
from DB_utils import db_register_user, username_exist

class SignUp(Action):
    def exec(self, conn):
        # print(f'Enter SignUp Action')

        # Read Username
        username = self.read_input(conn, "username")

        # 檢查用戶名是否已存在於數據庫中
        while username_exist(username):
            conn.send("Username exist, ".encode('utf-8'))
            username = self.read_input(conn, "another username")
        
        # Read Password
        pwd = self.read_input(conn, "password")


        # Read_email
        email = self.read_input(conn, "email")

        # Add to DB 將用戶名、密碼和電子郵件保存到數據庫中
        userid = db_register_user(username, pwd, email)
        conn.send(f'----------------------------------------\nSuccessfully create account! Userid = {userid}\n'.encode('utf-8'))

        return User(userid, username, pwd, email)
