
from .action import Action
from role.user import User
from DB_utils import db_register_user, account_exist

class SignUp(Action):
    def exec(self, conn):
        # print(f'Enter SignUp Action')

        # Read account
        account = self.read_input(conn, "account")

        # 檢查帳號是否已存在於數據庫中
        while account_exist(account):
            conn.send("此帳號已存在 Account already exist, ".encode('utf-8'))
            account = self.read_input(conn, "another account")
        
        # Read Username
        username = self.read_input(conn, "username")

        # Read nickname
        user_nickname = self.read_input(conn, "user_nickname")
        
        # Read Password
        pwd = self.read_input(conn, "password")

        # Read Nationality
        nationality = self.read_input(conn, "nationality")

        # Read City
        city = self.read_input(conn, "city")

        # Read Phone
        phone = self.read_input(conn, "phone")

        # Read Email
        email = self.read_input(conn, "email")

        # Read Sex
        sex = self.read_input(conn, "sex")

        # Read Birthday
        birthday = self.read_input(conn, "birthday")


        # Add to DB 將用戶名、密碼和電子郵件保存到數據庫中
        userid = db_register_user(username, user_nickname, pwd, nationality, city, phone, email, sex, birthday)
        conn.send(f'----------------------------------------\nSuccessfully create account! Userid = {userid}\n'.encode('utf-8'))

        return User(userid, account, username, user_nickname , pwd, nationality, city, phone, email, sex, birthday)
