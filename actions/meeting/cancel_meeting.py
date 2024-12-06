from ..Action import Action

class CancelMeetingAction(Action):
    def __init__(self):
        super().__init__("Cancel Meeting")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Cancel Meeting ===")
            
            meetings = db_manager.get_hosted_meetings(user.get_userid())
            if not meetings:
                self.send_message(conn, "You are not hosting any ongoing meetings.")
                return None
                
            self.send_message(conn, "\nYour hosted meetings:")
            for index, meeting in enumerate(meetings, 1):
                self.send_message(conn, 
                    f"{index}. {meeting['content']} at {meeting['event_place']} "
                    f"on {meeting['event_date']} ({meeting['num_participant']}/{meeting['max_participant']} participants)")
            
            choice = self.read_input(conn, "Select meeting to cancel (0 to go back)")
            if choice == "0":
                return None
                
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(meetings):
                self.send_message(conn, "Invalid choice!")
                return None
                
            meeting = meetings[int(choice) - 1]
            
            confirm = self.read_input(conn, "Are you sure you want to cancel this meeting? (y/n)")
            if confirm.lower() != 'y':
                self.send_message(conn, "Operation cancelled.")
                return None
            
            if db_manager.cancel_meeting(meeting['meeting_id']):
                self.send_message(conn, "Meeting has been successfully cancelled!")
            else:
                self.send_message(conn, "Failed to cancel the meeting!")
                
            return None
            
        except Exception as e:
            print(f"Error in cancel meeting: {e}")
            self.send_message(conn, "Failed to cancel meeting due to an error")
            return None
