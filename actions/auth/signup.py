from ..Action import Action
from datetime import datetime
from DB_utils import DatabaseManager as db_manager
from flask import request, jsonify, Blueprint

signUp = Blueprint("signUp", __name__)

class SignUpAction(Action):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def exec(self):
        try:
            account = request.form.get('account')
            # 確認帳號是否存在
            if self.db_manager and self.db_manager.check_account_exists(account):
                response = {
                    "status": "error",
                    "message": "Account already exists!",
                }
                return jsonify(response)

            password = request.form.get('password')          
            user_name = request.form.get('name')           
            user_nickname = request.form.get('nickname')                
            nationality = request.form.get('nationality')
            phone = request.form.get('phone')             
            email = request.form.get('email')         
            sex = request.form.get('gender')
            birthday = request.form.get('birthday')
            city = request.form.get('city')
            admin_code = request.form.get('admin code')

            if self.db_manager:
                success = self.db_manager.create_user(
                    account=account,
                    password=password,
                    user_name=user_name,
                    user_nickname=user_nickname,
                    nationality=nationality,
                    city=city,
                    phone=phone,
                    email=email,
                    sex=sex,
                    birthday=birthday,
                    register_time=datetime.now(),
                    admin_code = admin_code
                )
                
                if success:
                    response = {
                        "status": "success",
                        "message": "Registration successful!\nYou can now log in and add more personal details in your profile."
                    }
                    return jsonify(response)
                else:
                    response = {
                        "status": "error",
                        "message": "Registration failed!"
                    }
                    return jsonify(response)
            
            return jsonify({"status": "error", "message": "ERROR"})
            
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error in signup: {e}"
            }
            return jsonify(response)