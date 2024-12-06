from ..Action import Action

class PrivateChatAction(Action):
    def __init__(self):
        super().__init__("Private Chat")
        
    def exec(self, conn, db_manager=None):
        try:
            self.send_message(conn, "\n=== Private Chat ===")
            
            user_list = db_manager.get_available_users() 
            
            if not user_list:
                self.send_message(conn, "No users available for chat")
                return None
                
            self.send_message(conn, "\nAvailable users:")
            for index, user in enumerate(user_list, 1):
                self.send_message(conn, f"{index}. {user['nickname']}")
                
            choice = self.read_input(conn, "Select user to chat with (0 to exit)")
            
            if choice == "0":
                return None
                
            # Start chat
            # TODO: Implement chat logic
            
            return None
            
        except Exception as e:
            print(f"Error in private chat: {e}")
            self.send_message(conn, "Chat failed due to an error")
            return None
