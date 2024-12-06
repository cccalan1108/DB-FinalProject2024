from ..Action import Action

class FinishMeetingAction(Action):
    def __init__(self):
        super().__init__("Finish Meeting")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Finish Meeting ===")
            
            meetings = db_manager.get_hosted_meetings(user.get_userid())
            if not meetings:
                self.send_message(conn, "You are not hosting any ongoing meetings.")
                return None

            self.send_message(conn, "\nYour hosted meetings:")
            for idx, meeting in enumerate(meetings, 1):
                self.send_message(conn, 
                    f"{idx}. {meeting['content']} at {meeting['event_place']} "
                    f"on {meeting['event_date']} ({meeting['num_participant']}/{meeting['max_participant']} participants)")
            
            choice = self.read_input(conn, "Select meeting to finish (0 to go back)")
            if choice == "0":
                return None
                
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(meetings):
                self.send_message(conn, "Invalid choice!")
                return None
                
            meeting = meetings[int(choice) - 1]
            
            confirm = self.read_input(conn, "Are you sure you want to finish this meeting? (y/n)")
            if confirm.lower() != 'y':
                self.send_message(conn, "Operation cancelled.")
                return None
            
            if db_manager.finish_meeting(meeting['meeting_id']):
                self.send_message(conn, "Meeting has been successfully finished!")
            else:
                self.send_message(conn, "Failed to finish the meeting!")
                
            return None
            
        except Exception as e:
            print(f"Error in finish meeting: {e}")
            self.send_message(conn, "Failed to finish meeting due to an error")
            return None
