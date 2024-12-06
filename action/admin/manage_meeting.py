from ..Action import Action

class ManageMeetingAction(Action):
    def __init__(self):
        super().__init__("Manage Meetings")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== Manage Meetings ===")
                self.send_message(conn, "1. View All Meetings")
                self.send_message(conn, "2. Cancel Meeting")
                self.send_message(conn, "3. Force Finish Meeting")
                self.send_message(conn, "0. Back")
                
                choice = self.read_input(conn, "Select an option")
                
                if choice == "0":
                    return None
                    
                if choice == "1":
                    meetings = db_manager.get_all_meetings_admin()
                    if not meetings:
                        self.send_message(conn, "No meetings found.")
                        continue
                    self.send_table(conn, meetings)
                    
                elif choice == "2":
                    self._cancel_meeting(conn, db_manager)
                    
                elif choice == "3":
                    self._finish_meeting(conn, db_manager)
                    
                else:
                    self.send_message(conn, "Invalid choice!")
                    
        except Exception as e:
            print(f"Error in manage meetings: {e}")
            self.send_message(conn, "Operation failed due to an error")
            return None
            
    def _cancel_meeting(self, conn, db_manager):
        meeting_id = self.read_input(conn, "Enter meeting ID to cancel")
        
        if db_manager.admin_cancel_meeting(meeting_id):
            self.send_message(conn, "Meeting cancelled successfully!")
        else:
            self.send_message(conn, "Failed to cancel meeting!")
            
    def _finish_meeting(self, conn, db_manager):
        meeting_id = self.read_input(conn, "Enter meeting ID to finish")
        
        if db_manager.admin_finish_meeting(meeting_id):
            self.send_message(conn, "Meeting finished successfully!")
        else:
            self.send_message(conn, "Failed to finish meeting!") 