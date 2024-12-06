from .Role import Role
from actions.admin.manage_meeting import ManageMeetingAction
from actions.admin.manage_chat import ManageChatAction
from actions.admin.view_user_info import ViewUserInfoAction
from actions.admin.view_chat_history import ViewChatHistoryAction
from actions.auth.exit import ExitAction

class Admin(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)
        
        self.admin_action = [
            ManageMeetingAction(),
            ManageChatAction(),
            ViewUserInfoAction(),
            ViewChatHistoryAction(),
            ExitAction()
        ]
    
    def isAdmin(self):
        return True