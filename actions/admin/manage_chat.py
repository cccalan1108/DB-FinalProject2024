from ..Action import Action

class ManageChatAction(Action):
    def __init__(self):
        super().__init__("Manage Chats")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== View Meeting Chat Records ===")
                self.send_message(conn, "1. View Active Meetings")
                self.send_message(conn, "2. View Meeting Chat History")
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
                    self._view_meeting_chat(conn, db_manager)
                    
                else:
                    self.send_message(conn, "Invalid choice!")
                    
        except Exception as e:
            print(f"Error in manage chats: {e}")
            self.send_message(conn, "Operation failed due to an error")
            return None
            
    def _view_meeting_chat(self, conn, db_manager):
        meeting_id = self.read_input(conn, "Enter meeting ID")
        if not meeting_id.isdigit():
            self.send_message(conn, "Invalid meeting ID!")
            return
            
        messages = db_manager.get_meeting_messages(int(meeting_id))
        if not messages:
            self.send_message(conn, "No chat records found for this meeting.")
            return
            
        self.send_message(conn, "\n=== Meeting Chat Records ===")
        for msg in messages:
            sender_name = db_manager.get_user_nickname(msg[0])
            timestamp = msg[2].strftime('%Y-%m-%d %H:%M')
            self.send_message(conn, f"{sender_name}: {msg[1]} ({timestamp})")