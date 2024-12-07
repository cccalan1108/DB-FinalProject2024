from ..Action import Action
from datetime import datetime

class MeetingChatAction(Action):
    def __init__(self):
        super().__init__("Meeting Chat Room")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            self.send_message(conn, "\n=== Meeting Chat Room ===")
            
            meeting_list = db_manager.get_user_meetings(user.get_userid())  
            
            if not meeting_list:
                self.send_message(conn, "You are not participating in any meetings")
                return None
                
            self.send_message(conn, "\nYour meetings:")
            for index, meeting in enumerate(meeting_list, 1):
                self.send_message(conn, f"{index}. {meeting['content']} at {meeting['event_place']}")

            choice = self.read_input(conn, "Select meeting chat room (0 to exit)")
            
            if choice == "0" or not choice.isdigit():
                return None
                
            index = int(choice) - 1
            if index < 0 or index >= len(meeting_list):
                self.send_message(conn, "Invalid choice!")
                return None
                
            meeting = meeting_list[index]
            self._chat_session(conn, db_manager, user.get_userid(), meeting['meeting_id'])
            
            return None
            
        except Exception as e:
            print(f"Error in meeting chat: {e}")
            self.send_message(conn, "Chat failed due to an error")
            return None
            
    def _chat_session(self, conn, db_manager, user_id, meeting_id):
        try:
            self.send_message(conn, "[CHAT]=== Meeting Chat Room ===")
            messages = db_manager.get_meeting_messages(meeting_id)
            
            if messages:
                self.send_message(conn, "[CHAT]=== Recent Messages ===")
                for msg in messages:
                    timestamp = msg[2].strftime('%Y-%m-%d %H:%M')
                    sender_name = "You" if msg[0] == user_id else msg[3]
                    self.send_message(conn, f"[CHAT][{timestamp}] {sender_name}: {msg[1]}")
            
            self.send_message(conn, "[CHAT]Type 'exit' to end chat")
            conn.send("[CHAT_START]".encode('utf-8'))
            
            sender_nickname = db_manager.get_user_nickname(user_id)
            
            while True:
                message = self.read_input(conn, "[INPUT]Message")
                if message.lower() == 'exit':
                    conn.send("[CHAT_END]".encode('utf-8'))
                    break
                    
                if db_manager.send_meeting_message(meeting_id, user_id, message):
                    self.send_message(conn, "\rMessage sent!")

                    participants = db_manager.get_meeting_participants(meeting_id)
                    for participant in participants:
                        if participant != user_id:
                            self.server.broadcast_message(participant, 
                                f"[CHAT][Meeting] You received a message from {sender_nickname}: {message}")
                else:
                    self.send_message(conn, "[CHAT]Failed to send message!")
                    
        except Exception as e:
            print(f"Error in meeting chat session: {e}")
            self.send_message(conn, "[CHAT]Chat session ended due to an error")