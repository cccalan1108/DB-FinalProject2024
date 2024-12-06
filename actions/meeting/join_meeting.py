from ..Action import Action

class JoinMeetingAction(Action):
    def __init__(self):
        super().__init__("Join Meeting")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Join Meeting ===")
            
            meeting_id = self.read_input(conn, "Enter meeting ID to join (0 to cancel)")
            if meeting_id == "0":
                return None
                
            if not meeting_id.isdigit():
                self.send_message(conn, "Invalid meeting ID!")
                return None
                
            meeting = db_manager.check_meeting_availability(int(meeting_id))
            if not meeting:
                self.send_message(conn, "Meeting not found or not available!")
                return None
                
            if db_manager.is_user_in_meeting(user.get_userid(), int(meeting_id)):
                self.send_message(conn, "You are already in this meeting!")
                return None
                
            if db_manager.join_meeting(user.get_userid(), int(meeting_id)):
                self.send_message(conn, "Successfully joined the meeting!")
            else:
                self.send_message(conn, "Failed to join the meeting!")
                
            return None
            
        except Exception as e:
            print(f"Error in join meeting: {e}")
            self.send_message(conn, "Failed to join meeting due to an error")
            return None