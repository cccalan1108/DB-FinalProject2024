from ..Action import Action
from datetime import datetime

class CreateMeetingAction(Action):
    MEETING_TYPES = ['午餐', '咖啡/下午茶', '晚餐', '喝酒', '語言交換']
    LANGUAGES = ['中文', '台語', '客語', '原住民語', '英文', '日文', '韓文', 
                '法文', '德文', '西班牙文', '俄文', '阿拉伯文', '泰文', '越南文', '印尼文']
    
    def __init__(self):
        super().__init__("Create Meeting")
        
    def exec(self, conn, db_manager=None, user=None):
        self.send_message(conn, "\n=== Create New Meeting ===")
        
        self.send_message(conn, "\nMeeting Types:")
        for i, type_ in enumerate(self.MEETING_TYPES, 1):
            self.send_message(conn, f"{i}. {type_}")
        
        choice = self.read_input(conn, "Select meeting type")
        while not choice.isdigit() or int(choice) not in range(1, len(self.MEETING_TYPES) + 1):
            self.send_message(conn, "Invalid choice! Please try again.")
            choice = self.read_input(conn, "Select meeting type")
        content = self.MEETING_TYPES[int(choice) - 1]
        
        self.send_message(conn, "\nAvailable Languages (separate multiple choices with comma):")
        for i, lang in enumerate(self.LANGUAGES, 1):
            self.send_message(conn, f"{i}. {lang}")
        
        choices = self.read_input(conn, "Select languages (e.g., 1,3,5)")
        languages = []
        for c in choices.split(','):
            idx = int(c.strip())
            if 1 <= idx <= len(self.LANGUAGES):
                languages.append(self.LANGUAGES[idx - 1])
                
        if not languages:
            self.send_message(conn, "At least one language must be selected!")
            return None
        
        city = self.read_input(conn, "City (max 20 characters)")
        while len(city) > 20 or len(city) == 0:
            self.send_message(conn, "City must be between 1 and 20 characters")
            city = self.read_input(conn, "City")
            
        place = self.read_input(conn, "Place/Address (max 50 characters)")
        while len(place) > 50 or len(place) == 0:
            self.send_message(conn, "Place must be between 1 and 50 characters")
            place = self.read_input(conn, "Place/Address")
        
        date = self.read_input(conn, "Date (YYYY-MM-DD)")
        start_time = self.read_input(conn, "Start time (HH:MM)")
        end_time = self.read_input(conn, "End time (HH:MM)")
        
        max_participants = self.read_input(conn, "Maximum number of participants")
        while not max_participants.isdigit() or int(max_participants) < 2:
            self.send_message(conn, "Maximum participants must be at least 2!")
            max_participants = self.read_input(conn, "Maximum number of participants")
            
        meeting_id = db_manager.create_meeting(
            holder_id=user.get_userid(),
            content=content,
            event_date=date,
            start_time=start_time,
            end_time=end_time,
            event_city=city,
            event_place=place,
            max_participants=int(max_participants),
            languages=languages
        )
        
        if meeting_id:
            self.send_message(conn, "Meeting created successfully!")
        else:
            self.send_message(conn, "Failed to create meeting!")
        
        return None