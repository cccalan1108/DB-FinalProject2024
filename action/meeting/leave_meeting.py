from ..Action import Action  

class LeaveMeetingAction(Action):
    def __init__(self):
        super().__init__("Leave Meeting")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Leave Meeting ===")
            
            meetings = db_manager.get_user_meetings(user.get_userid())
            if not meetings:
                self.send_message(conn, "You are not participating in any meetings.")
                return None
            
            choice = self.read_input(conn, "Select meeting to leave (0 to cancel)")
            if choice == "0":
                return None
                
            meeting = meetings[int(choice) - 1]
            
            if meeting['holder_id'] == user.get_userid():
                self.send_message(conn, "As the meeting holder, you cannot leave the meeting. You can cancel it instead.")
                return None
            
            if db_manager.leave_meeting(user.get_userid(), meeting['meeting_id']):
                self.send_message(conn, "Successfully left the meeting!")
            else:
                self.send_message(conn, "Failed to leave the meeting!")
                
            return None
            
        except Exception as e:
            print(f"Error in leave meeting: {e}")
            self.send_message(conn, "Failed to leave meeting due to an error")
            return None