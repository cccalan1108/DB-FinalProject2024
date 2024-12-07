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
                self.send_message(conn, "4. Remove User from Meeting")
                self.send_message(conn, "0. Back")
                
                choice = self.read_input(conn, "Select an option")
                
                if choice == "0":
                    return None
                    
                if choice == "1":
                    meetings = db_manager.get_all_meetings_admin()
                    if not meetings:
                        self.send_message(conn, "No active meetings found.")
                        continue
                    self.send_table(conn, meetings)
                    
                elif choice == "2":
                    self._cancel_meeting(conn, db_manager)
                    
                elif choice == "3":
                    self._finish_meeting(conn, db_manager)
                    
                elif choice == "4":
                    self._remove_user_from_meeting(conn, db_manager)
                    
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
            
    def _remove_user_from_meeting(self, conn, db_manager):
        meeting_id = self.read_input(conn, "Enter meeting ID")
        if not meeting_id.isdigit():
            self.send_message(conn, "Invalid meeting ID!")
            return
            
        user_id = self.read_input(conn, "Enter user ID to remove")
        if not user_id.isdigit():
            self.send_message(conn, "Invalid user ID!")
            return
            
        if db_manager.leave_meeting(int(user_id), int(meeting_id)):
            self.send_message(conn, "User removed from meeting successfully!")
            self.server.broadcast_message(int(user_id), 
                f"You have been removed from meeting {meeting_id} by admin")
        else:
            self.send_message(conn, "Failed to remove user from meeting!") 