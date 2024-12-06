from ..Action import Action  

class ViewHistoryAction(Action):
    def __init__(self):
        super().__init__("View Meeting History")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Meeting History ===\n")
            
            history = db_manager.get_user_meeting_history(user.get_userid())
            if not history:
                self.send_message(conn, "No meeting history found.")
                return None
                
            self.send_table(conn, history)
            return None
            
        except Exception as e:
            print(f"Error in view history: {e}")
            self.send_message(conn, "Failed to view history due to an error")
            return None