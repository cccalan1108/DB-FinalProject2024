from ..Action import Action

class ViewUserInfoAction(Action):
    def __init__(self):
        super().__init__("View User Information")
        
    def exec(self, conn, db_manager=None, user=None):
        try:
            while True:
                self.send_message(conn, "\n=== View User Information ===")
                self.send_message(conn, "1. List All Users")
                self.send_message(conn, "2. View Basic Information")
                self.send_message(conn, "3. View Meeting History")
                self.send_message(conn, "0. Back")
                
                choice = self.read_input(conn, "Select an option")
                
                if choice == "0":
                    return None
                
                if choice == "1":
                    users = db_manager.get_all_non_admin_users()
                    if users:
                        self.send_table(conn, users)
                    else:
                        self.send_message(conn, "No users found.")
                    continue
                    
                user_id = self.read_input(conn, "Enter user ID")
                if not user_id.isdigit():
                    self.send_message(conn, "Invalid user ID!")
                    continue
                
                if choice == "2":
                    info = db_manager.get_user_info(user_id)
                    if not info:
                        self.send_message(conn, "User not found.")
                        continue
                    self.send_table(conn, info)
                    
                elif choice == "3":
                    history = db_manager.get_user_meeting_history(user_id)
                    if not history:
                        self.send_message(conn, "No meeting history found.")
                        continue
                    self.send_table(conn, history)
                else:
                    self.send_message(conn, "Invalid choice!")
                    
        except Exception as e:
            print(f"Error in view user info: {e}")
            self.send_message(conn, "Operation failed due to an error")
            return None