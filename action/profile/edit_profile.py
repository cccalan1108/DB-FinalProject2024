from ..Action import Action  

class EditProfileAction(Action):
    PROFILE_OPTIONS = {
        'Star_sign': {
            'name': 'Star Sign (星座)',
            'options': ['摩羯', '水瓶', '雙魚', '牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手']
        },
        'Mbti': {
            'name': 'MBTI',
            'options': ['ISTP', 'ISFP', 'ESTP', 'ESFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 
                       'INTP', 'INTJ', 'ENTP', 'ENTJ', 'INFJ', 'INFP', 'ENFJ', 'ENFP']
        },
        'Blood_type': {
            'name': 'Blood Type (血型)',
            'options': ['A', 'B', 'AB', 'O']
        },
        'Religion': {
            'name': 'Religion (宗教)',
            'options': ['無', '佛教', '道教', '基督教', '天主教', '伊斯蘭教', '印度教', '其他']
        },
        'University': {
            'name': 'University (大學)'
        },
        'Married': {
            'name': 'Marital Status (婚姻狀況)',
            'options': ['未婚', '已婚', '喪偶']
        },
        'Sns': {
            'name': 'SNS Status (社交媒體狀態)',
            'options': ['YES', 'NO']
        },
        'Self_introduction': {
            'name': 'Self Introduction (自我介紹)'
        },
        'Interest': {
            'name': 'Interests (興趣)'
        },
        'Find_meeting_type': {
            'name': 'Meeting Preferences (期望聚會類型)',
        }
    }

    def __init__(self):
        super().__init__("Edit Profile")

    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self._show_menu(conn)
                choice = self.read_input(conn, "Your choice")
                
                if choice == "0":
                    break
                    
                if not choice.isdigit() or int(choice) not in range(1, len(self.PROFILE_OPTIONS) + 1):
                    self.send_message(conn, "Invalid option! Please try again.")
                    continue
                
                field = list(self.PROFILE_OPTIONS.keys())[int(choice) - 1]
                self._handle_edit(conn, db_manager, field, user.get_userid())
            
            return None
            
        except Exception as e:
            print(f"Error in edit profile: {e}")
            self.send_message(conn, "Failed to edit profile")
            return None

    def _show_menu(self, conn):
        self.send_message(conn, "\n=== Edit Profile ===")
        for i, (_, info) in enumerate(self.PROFILE_OPTIONS.items(), 1):
            self.send_message(conn, f"{i}. {info['name']}")
        self.send_message(conn, "0. Back to Main Menu")

    def _handle_edit(self, conn, db_manager, field, user_id):
        field_info = self.PROFILE_OPTIONS[field]
        
        if 'options' in field_info:
            self._handle_option_field(conn, db_manager, field, field_info, user_id)
        else:
            self._handle_text_field(conn, db_manager, field, field_info, user_id)

    def _handle_option_field(self, conn, db_manager, field, field_info, user_id):
        self.send_message(conn, f"\nAvailable {field_info['name']}:")
        for i, option in enumerate(field_info['options'], 1):
            self.send_message(conn, f"{i}. {option}")
            
        choice = self.read_input(conn, f"Select your {field_info['name']} (0 to cancel)")
        if choice == "0":
            return
            
        if choice.isdigit() and 1 <= int(choice) <= len(field_info['options']):
            value = field_info['options'][int(choice) - 1]
            if field == 'Sns' and value == 'YES':
                if db_manager.update_user_detail(field, value, user_id):
                    self.send_message(conn, f"{field_info['name']} updated successfully!")
                    self._handle_sns_detail(conn, db_manager, user_id)
                else:
                    self.send_message(conn, f"Failed to update {field_info['name']}")
            else:
                if db_manager.update_user_detail(field, value, user_id):
                    self.send_message(conn, f"{field_info['name']} updated successfully!")
                else:
                    self.send_message(conn, f"Failed to update {field_info['name']}")
        else:
            self.send_message(conn, "Invalid choice")

    def _handle_text_field(self, conn, db_manager, field, field_info, user_id):
        value = self.read_input(conn, f"Enter your {field_info['name']} (0 to cancel)")
        if value == "0":
            return
            
        if db_manager.update_user_detail(field, value, user_id):
            self.send_message(conn, f"{field_info['name']} updated successfully!")
        else:
            self.send_message(conn, f"Failed to update {field_info['name']}")

    def _handle_sns_detail(self, conn, db_manager, user_id):
        self.send_message(conn, "\nAvailable SNS platforms:")
        sns_platforms = ['Facebook', 'Instagram', 'Threads', 'X', 'Tiktok', 
                        '小紅書', 'WhatsApp', 'LINE', 'WeChat', 'KakaoTalk']
        
        while True:
            for i, platform in enumerate(sns_platforms, 1):
                self.send_message(conn, f"{i}. {platform}")
            self.send_message(conn, "0. Back")
            
            choice = self.read_input(conn, "Select platform (0 to finish)")
            if choice == "0":
                break
            
            if not choice.isdigit() or int(choice) not in range(1, len(sns_platforms) + 1):
                self.send_message(conn, "Invalid choice!")
                continue
            
            platform = sns_platforms[int(choice) - 1]
            sns_id = self.read_input(conn, f"Enter your {platform} ID/username")
            
            if db_manager.add_sns_detail(user_id, platform, sns_id):
                self.send_message(conn, f"{platform} account added successfully!")
            else:
                self.send_message(conn, f"Failed to add {platform} account")