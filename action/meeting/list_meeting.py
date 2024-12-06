from ..Action import Action  

class ListMeetingAction(Action):
    def __init__(self):
        super().__init__("List Meeting")
        
    def exec(self, conn, db_manager=None, **kwargs):
        self.send_message(conn, "\n=== Available Meetings ===\n")
            
        meetings = db_manager.get_all_meetings()
        if not meetings:
            self.send_message(conn, "No available meetings found.")
            return None
        self.send_table(conn, meetings)

        return None