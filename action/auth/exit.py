from ..Action import Action  

class ExitAction(Action):
    def __init__(self):
        super().__init__("Exit")
        
    def exec(self, conn, db_manager=None, user=None):
        self.send_message(conn, "Goodbye!")
        if user is None:
            return "exit"
        else:
            return "logout" 
