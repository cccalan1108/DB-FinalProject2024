class Role:
    def __init__(self, userid, username, pwd, email):
        self._userid = userid
        self._username = username
        self._pwd = pwd
        self._email = email
    
    def get_userid(self):
        return self._userid
        
    def get_username(self):
        return self._username
        
    def get_actions(self):
        if hasattr(self, 'admin_action'):
            return self.admin_action
        elif hasattr(self, 'user_action'):
            return self.user_action
        return []