from .Role import Role
from actions.profile.edit_profile import EditProfileAction
from actions.meeting.create_meeting import CreateMeetingAction
from actions.meeting.list_meeting import ListMeetingAction
from actions.meeting.join_meeting import JoinMeetingAction 
from actions.meeting.leave_meeting import LeaveMeetingAction
from actions.meeting.cancel_meeting import CancelMeetingAction 
from actions.meeting.finish_meeting import FinishMeetingAction
from actions.meeting.view_history import ViewHistoryAction
from actions.chat.private_chat import PrivateChatAction
from actions.chat.meeting_chat import MeetingChatAction
from actions.auth.exit import ExitAction

class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)
        
        self.user_action = [
            EditProfileAction(),
            CreateMeetingAction(),
            ListMeetingAction(),
            JoinMeetingAction(),
            LeaveMeetingAction(),
            CancelMeetingAction(),
            FinishMeetingAction(),
            ViewHistoryAction(),
            PrivateChatAction(),
            MeetingChatAction(),
            ExitAction()
        ]