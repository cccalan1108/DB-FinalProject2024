class Role():
    def __init__(self,userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, registertime):
        self.userid = userid
        self.username = username
        self.usernickname = usernickname
        self.pwd = pwd
        self.nationality = nationality
        self.city = city
        self.phone = phone
        self.email = email
        self.sex = sex
        self.birthday = birthday
        self.registertime = registertime
        self.user_action = []


    def get_available_action(self):
        pass
    def get_username(self):
        return self.username
    def get_userid(self):
        return self.userid
    def get_usernickname(self):
        return self.usernickname
    def get_nationality (self):
        return self.nationality 
    def get_city(self):
        return self.city
    def get_phone(self):
        return self.phone
    def get_email(self):
        return self.email
    def get_sex(self):
        return self.sex
    def get_birthday(self):
        return self.birthday
    def get_registertime(self):
        return self.registertime
    def get_available_action(self):
        return self.user_action
    
    
    def get_info_msg_no_pwd(self):
        return f'userid: {self.userid}, username: {self.username}, email: {self.email}, role: {type(self).__name__}'
    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}, role: {type(self).__name__}'
    def isAdmin(self):
        return False