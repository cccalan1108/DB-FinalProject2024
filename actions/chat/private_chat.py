from ..Action import Action
from datetime import datetime

class PrivateChatAction(Action):
    def __init__(self):
        super().__init__("Private Chat")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== Private Chat ===")
                self.send_message(conn, "")
                self.send_message(conn, "1. Start New Chat")
                self.send_message(conn, "2. View Chat History")
                self.send_message(conn, "0. Back")
                
                choice = self.read_input(conn, "Select an option")
                
                if choice == "0":
                    return None
                elif choice == "1":
                    self._start_new_chat(conn, db_manager, user)
                elif choice == "2":
                    self._view_chat_history(conn, db_manager, user)
                else:
                    self.send_message(conn, "Invalid choice!")
                    
        except Exception as e:
            print(f"Error in private chat: {e}")
            self.send_message(conn, "Chat failed due to an error")
            return None
            
    def _start_new_chat(self, conn, db_manager, user):
        user_list = db_manager.get_available_users(user.get_userid())
        if not user_list:
            self.send_message(conn, "No users available for chat")
            return
            
        self.send_message(conn, "\nAvailable users:")
        for index, other_user in enumerate(user_list, 1):
            self.send_message(conn, f"{index}. {other_user['nickname']}")
            
        choice = self.read_input(conn, "Select user to chat with (0 to exit)")
        if choice == "0" or not choice.isdigit():
            return
            
        index = int(choice) - 1
        if index < 0 or index >= len(user_list):
            self.send_message(conn, "Invalid choice!")
            return
            
        other_user = user_list[index]
        
        if db_manager.is_admin(other_user['user_id']):
            self.send_message(conn, "Cannot start private chat with admin users!")
            return
        
        self._chat_session(conn, db_manager, user.get_userid(), other_user['user_id'])
        
    def _chat_session(self, conn, db_manager, sender_id, receiver_id):
        try:
            self.send_message(conn, "\n=== Chat Session ===")
            messages = db_manager.get_private_messages(sender_id, receiver_id)
            
            if messages:
                self.send_message(conn, "[CHAT]=== Recent Messages ===")
                for msg in messages:
                    timestamp = msg[2].strftime('%Y-%m-%d %H:%M')
                    sender_name = "You" if msg[0] == sender_id else msg[3]
                    self.send_message(conn, f"[CHAT][{timestamp}] {sender_name}: {msg[1]}")
            
            self.send_message(conn, "[CHAT]Type 'exit' to end chat")
            conn.send("[CHAT_START]".encode('utf-8'))
            
            sender_nickname = db_manager.get_user_nickname(sender_id)
            
            while True:
                message = self.read_input(conn, "Message")
                if message.lower() == 'exit':
                    conn.send("[CHAT_END]".encode('utf-8'))
                    break
                    
                if db_manager.send_private_message(sender_id, receiver_id, message):
                    self.send_message(conn, "\rMessage sent!")
                    
                    self.server.broadcast_message(receiver_id, 
                        f"You received a message from {sender_nickname}: {message}")
                else:
                    self.send_message(conn, "[CHAT]Failed to send message!")
        except Exception as e:
            print(f"Error in chat session: {e}")
            self.send_message(conn, "[CHAT]Chat session ended due to an error")
    def _view_chat_history(self, conn, db_manager, user):
        chat_records = db_manager.get_user_chat_records(user.get_userid())
        if not chat_records:
            self.send_message(conn, "No chat records found")
            return
        
        self.send_message(conn, "\nChat records:")
        for index, record in enumerate(chat_records, 1):
            self.send_message(conn, f"{index}. Chat with {record['chat_name']} (Last: {record['last_time'].strftime('%Y-%m-%d %H:%M')})")
        
        choice = self.read_input(conn, "Select chat to view (0 to go back)")
        if choice == "0" or not choice.isdigit():
            return
        
        index = int(choice) - 1
        if index < 0 or index >= len(chat_records):
            self.send_message(conn, "Invalid choice!")
            return
        
        record = chat_records[index]
        chat_history = db_manager.get_chat_history(user.get_userid(), record['chat_id'])
        if chat_history:
            self.send_table(conn, chat_history)
        else:
            self.send_message(conn, "No messages found.")