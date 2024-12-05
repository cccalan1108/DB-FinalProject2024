from .action import Action
from DB_utils import find_meeting
class FindMeeting(Action):
    def exec(self, conn, user):
        print("為您找尋聚會 Find Meeting")
        conn.send(" (enter None if don't want to search based on the item)\n".encode('utf-8'))
        event_city= self.read_input(conn, "event_city")
        content = self.read_input(conn, "content")
        print(f'Find Course | {event_city}, {content}')
        
        table = find_meeting(event_city, content)
        self.send_table(conn, table)
    
        return 