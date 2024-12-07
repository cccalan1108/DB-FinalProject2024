from ..Action import Action

class ViewChatHistoryAction(Action):
    def __init__(self):
        super().__init__("View Chat History")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== View Chat History ===")
                
                user_id = self.read_input(conn, "Enter user ID (0 to go back)")
                
                if user_id == "0":
                    return None
                    
                if not user_id.isdigit():
                    self.send_message(conn, "Invalid user ID!")
                    continue
                
                chat_records = db_manager.get_user_chat_records(user_id)
                if not chat_records:
                    self.send_message(conn, "No chat records found.")
                    continue
                    
                self.send_message(conn, "\nChat records:")
                for index, record in enumerate(chat_records, 1):
                    self.send_message(conn, f"{index}. Chat with {record['chat_name']} (Last: {record['last_time'].strftime('%Y-%m-%d %H:%M')})")
                
                choice = self.read_input(conn, "Select chat to view (0 to go back)")
                if choice == "0" or not choice.isdigit():
                    continue
                    
                index = int(choice) - 1
                if index < 0 or index >= len(chat_records):
                    self.send_message(conn, "Invalid choice!")
                    continue
                    
                record = chat_records[index]
                chat_history = db_manager.get_chat_history(user_id, record['chat_id'])
                if chat_history:
                    self.send_table(conn, chat_history)
                else:
                    self.send_message(conn, "No messages found.")
                    
        except Exception as e:
            print(f"Error in view chat history: {e}")
            self.send_message(conn, "Operation failed due to an error")
            return None