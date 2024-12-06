from ..Action import Action

class MeetingChatAction(Action):
    def __init__(self):
        super().__init__("Meeting Chat Room")
        
    def exec(self, conn, db_manager=None):
        try:
            self.send_message(conn, "\n=== Meeting Chat Room ===")
            

            meeting_list = db_manager.get_user_meetings()  
            
            if not meeting_list:
                self.send_message(conn, "You are not participating in any meetings")
                return None
                
            self.send_message(conn, "\nYour meetings:")
            for index, meeting in enumerate(meeting_list, 1):
                self.send_message(conn, f"{index}. {meeting['content']} at {meeting['event_place']}")

            choice = self.read_input(conn, "Select meeting chat room (0 to exit)")
            
            if choice == "0":
                return None
                
            # Start chat
            # TODO: Implement chat logic
            
            return None
            
        except Exception as e:
            print(f"Error in meeting chat: {e}")
            self.send_message(conn, "Chat failed due to an error")
            return None
