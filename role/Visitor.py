from actions.auth.signup import SignUpAction
from actions.auth.login import LoginAction
from actions.auth.exit import ExitAction
from .Role import Role

class Visitor(Role):
    def __init__(self):
        super().__init__(None, "visitor", None, None)
        self.visitor_actions = [
            SignUpAction(),
            LoginAction(),
            ExitAction()
        ]
    def get_visitor_actions(self):
        return self.visitor_actions