from enum import Enum
from datetime import datetime
#import bcrypt

class Gender(Enum):
    MALE = "男 Male"
    FEMALE = "女 Female"
    OTHER = "其他 Other"

class StarSign(Enum):
    ARIES = "牡羊 Aries" 
    TAURUS = "金牛 Taurus" 
    GEMINI = "雙子 Gemini" 
    CANCER = "巨蟹 Cancer" 
    LEO = "獅子 Leo" 
    VIRGO = "處女 Virgo"
    LIBRA = "天秤 Libra"
    SCORPIO = "天蠍 Scorpio"
    SAGITTARIUS = "射手 Sagittarius"
    CAPRICORN = "摩羯 Capricorn"
    AQUARIUS = "水瓶 Caprisorn"
    PISCES = "雙魚 Pisces"

class Mbti(Enum):
    ISTP = "鑑賞家 ISTP" 
    ISFP = "探險家 ISFP" 
    ESTP = "企業家 ESTP" 
    ESFP = "表演者 ESFP" 
    ISTJ = "物流師 ISTJ" 
    ISFJ = "守衛者 ISFJ"
    ESTJ = "總經理 ESTJ"
    ESFJ = "執政官 ESFJ"
    INTJ = "建築師 INTJ"
    INTP = "邏輯家 INTP"
    ENTJ = "指揮官 ENTJ"
    ENTP = "辯論家 ENTP"
    INFJ = "提倡者 INFJ"
    INFP = "調停者 INFP"
    ENFJ = "主人公 ENFJ"
    ENFP = "競選者 ENFP"

class BloodType(Enum):
    TYPEA = "A 型" 
    TYPEB = "B 型" 
    TYPEO = "O 型" 
    TYPEAB = "AB 型" 

class Religion(Enum):
    NONE = "無信仰 No Religion" 
    BUDDHISM = "佛教 Buddhism" 
    TAOISM = "道教 Taoism" 
    ISLAM = "伊斯蘭教 Islam" 
    HINDUISM = "印度教 Hinduism"
    EASTERNORTHODOXY = "東正教 Eastern Orthodoxy"
    CHRISTIANITY = "基督教 Christianity"
    CATHOLICISM = "天主教 Catholicism"
    JUDAIM = "猶太教 Judaism"
    MORMONISM = "摩門教 Mormonism"
    ELSE = "其他 Else"

class Married(Enum):
    SINGLE = "單身 Single" 
    MARRIED = "已婚 Married" 
    DIVORCE = "離婚 Divorce"
    WIDOWED = "喪偶 Widowed"

class Sns(Enum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    THREADS = "Threads"
    TWITTER = "X (Twitter)"
    LINE = "Line"
    KAKAOTALK = "KakaoTalk"
    WHATSAPP = "WhatsApp"


class Role:
    def __init__(self, userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, registertime,
                 star_sign=None, mbti=None, blood_type=None, religion=None, university=None, married=None, sns=None):
        self.userid = userid
        self.username = username
        self.usernickname = usernickname
        #self.pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        self.pwd = pwd
        self.nationality = nationality
        self.city = city
        self.phone = phone
        self.email = email
        self.sex = Gender(sex)
        self.birthday = birthday
        self.registertime = registertime
        self.star_sign = StarSign(star_sign) if star_sign else None
        self.mbti = Mbti(mbti) if mbti else None
        self.blood_type = BloodType(blood_type) if blood_type else None
        self.religion = Religion(religion) if religion else None
        self.university = university
        self.married = Married(married) if married else None
        self.sns = sns if sns else []
        self.user_action = []



    # def get_available_action(self):
    #     pass
    def get_available_action(self): # 返回用戶當前可以執行的操作列表（self.user_action）
        return self.user_action
    def get_username(self): # 返回用戶名（self.username）
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
    
    #  屬性輸出的格式化處理
    def get_full_info(self, include_pwd=False):
        info = {
            "userid": self.userid,
            "username": self.username,
            "usernickname": self.usernickname,
            "email": self.email,
            "nationality": self.nationality,
            "city": self.city,
            "phone": self.phone,
            "sex": self.sex.value,
            "birthday": self.birthday,
            "registertime": self.registertime,
            "star_sign": self.star_sign.value if self.star_sign else None,
            "mbti": self.mbti.value if self.mbti else None,
            "blood_type": self.blood_type.value if self.blood_type else None,
            "religion": self.religion.value if self.religion else None,
            "university": self.university,
            "married": self.married.value if self.married else None,
            "sns": [f"{sns['type']}: {sns['id']}" for sns in self.sns] if self.sns else None,
        }
        if include_pwd:
            info["pwd"] = self.pwd
        return {k: v for k, v in info.items() if v is not None}


    
    # SNS 相關
    def add_sns(self, sns_type, sns_id):
        """"新增 SNS 資訊"""
        try:
            sns_type_enum = Sns[sns_type.upper()]  # 驗證 SNS 類型是否有效
        except KeyError:
            raise ValueError(f"Invalid SNS type: {sns_type}. Must be one of {[e.value for e in Sns]}")

        if any(sns["type"] == sns_type_enum.value for sns in self.sns):
            raise ValueError(f"SNS type {sns_type_enum.value} already exists for this user.")

        self.sns.append({"type": sns_type_enum.value, "id": sns_id})

    def remove_sns(self, sns_type):
        """移除 SNS 資訊"""
        try:
            sns_type_enum = Sns[sns_type.upper()]  # 驗證 SNS 類型是否有效
        except KeyError:
            raise ValueError(f"Invalid SNS type: {sns_type}. Must be one of {[e.value for e in Sns]}")

        self.sns = [sns for sns in self.sns if sns["type"] != sns_type_enum.value]


    def get_sns(self):
        """獲取所有 SNS 資訊"""
        return self.sns

    def get_sns_by_type(self, sns_type):
        """根據類型查找 SNS 資訊"""
        try:
            sns_type_enum = Sns[sns_type.upper()]
        except KeyError:
            raise ValueError(f"Invalid SNS type: {sns_type}. Must be one of {[e.value for e in Sns]}")

        for sns in self.sns:
            if sns["type"] == sns_type_enum.value:
                return sns
        raise ValueError(f"SNS type {sns_type_enum.value} not found for this user.")


    


    def get_info_msg_no_pwd(self):
        return f'userid: {self.userid}, username: {self.username}, email: {self.email}, role: {type(self).__name__}'
    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, email: {self.email}, role: {type(self).__name__}'
    def isAdmin(self):
        return False