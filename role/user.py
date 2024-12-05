from .role import Role
from action.exit import Exit
from action.logout import Logout
from action.event.createMeeting import CreateEvent
from action.event.listMeeting import ListEvent
from action.event.joinMeeting import JoinEvent
from action.event.leaveMeeting import LeaveEvent
from action.listHistory import ListHistory
from action.findReserved import FindReserved
from action.modifyUserInfo import ModifyUserInfo

class User(Role):
    def __init__(self, userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, registertime,
                 star_sign=None, mbti=None, blood_type=None, religion=None, university=None, married=None, sns=None):
        super().__init__(userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, registertime,
                         star_sign, mbti, blood_type, religion, university, married, sns)
        
        self.user_action = [
            CreateEvent("Create Meeting"),
            ListEvent("List Meetings"),
            JoinEvent("Join Meeting"),
            LeaveEvent("Leave Meeting"),
            ListHistory("View History"),
            FindReserved("Find Reserved Classroom"),
            ModifyUserInfo("Modify User Info"),
            Logout("Logout"),
            Exit("Exit System"),
        ]
