from ..Action import Action

class ViewChatHistoryAction(Action):
    def __init__(self):
        super().__init__("View Chat History")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== View Chat History ===")
                self.send_message(conn, "0. Back")
                
                user_id = self.read_input(conn, "Enter user ID (0 to go back)")
                
                if user_id == "0":
                    return None
                    
                if not user_id.isdigit():
                    self.send_message(conn, "Invalid user ID!")
                    continue
                
                chats = db_manager.get_user_chat_history(user_id)
                if not chats:
                    self.send_message(conn, "No chat history found.")
                    continue
                self.send_table(conn, chats)
                    
        except Exception as e:
            print(f"Error in view chat history: {e}")
            self.send_message(conn, "Operation failed due to an error")
            return None