from .role import Role
from action.exit import Exit
from action.logout import Logout
from action.event.createMeeting import CreateEvent
from action.event.listMeeting import ListEvent
from action.event.joinMeeting import JoinEvent
from action.event.leaveMeeting import LeaveEvent
from action.listHistory import ListHistory
#from action.FindCourse import FindCourse
from action.findReserved import FindReserved
from action.modifyUserInfo import ModifyUserInfo


# 繼承 Role 
class User(Role):
    def __init__(self, userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, register_time):
        super().__init__(userid, username, usernickname, pwd, nationality, city, phone, email, sex, birthday, register_time)

        self.user_action =  [
                                CreateEvent("Create Study Event"),
                                ListEvent("List All Available Study Events"),
                                JoinEvent("Join Study Event"),
                                LeaveEvent("Leave Study Event"),
                                ListHistory("List Study Group History"),
                                #FindCourse("Find Course"),
                                FindReserved("Find Reserved Classroom"),
                                ModifyUserInfo("Modify User Information"),
                                Logout("Logout"),
                                Exit("Leave System")
                            ]
        
