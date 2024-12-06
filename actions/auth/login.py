from ..Action import Action
from role.User import User
from role.Admin import Admin

class LoginAction(Action):
    def __init__(self):
        super().__init__("Login")
        
    def exec(self, conn, db_manager=None):
        account = self.read_input(conn, "Enter your account")
        password = self.read_input(conn, "Enter your password")
        
        result = db_manager.verify_login(account, password)
        if result:
            self.send_message(conn, f"\nWelcome back, {result['user_name']}!")
            self.send_message(conn, f"Your ID is: {result['user_id']}")
            
            if result['role'] == 'Admin':
                user = Admin(result['user_id'], result['user_name'], 
                           password, result['email'])
            else:
                user = User(result['user_id'], result['user_name'], 
                          password, result['email'])
            return user
        
        self.send_message(conn, "Invalid account or password!")
        return None
        