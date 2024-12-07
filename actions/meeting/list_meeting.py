# from ..Action import Action  

# class ListMeetingAction(Action):
#     def __init__(self):
#         super().__init__("List Meeting")
        
#     def exec(self, conn, db_manager=None, **kwargs):
#         self.send_message(conn, "\n=== Available Meetings ===\n")
            
#         meetings = db_manager.get_all_meetings()
#         if not meetings:
#             self.send_message(conn, "No available meetings found.")
#             return None
#         self.send_table(conn, meetings)

#         return None


from flask import Blueprint, jsonify
from DB_utils import DatabaseManager

list_meeting = Blueprint("list_meeting", __name__)

class ListMeetingAction:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def exec(self):
        try:
            # 獲取所有會議資料
            meetings = self.db_manager.get_all_meetings()
            if not meetings:
                return jsonify({"status": "error", "message": "No available meetings found"}), 404

            # 按欄位順序轉換為 JSON 格式
            meetings_list = [
                {
                    "meeting_id": row["meeting_id"],
                    "content": row["content"],
                    "event_date": row["event_date"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "event_city": row["event_city"],
                    "event_place": row["event_place"],
                    "status": row["status"],
                    "num_participant": row["num_participant"],
                    "max_participant": row["max_participant"],
                    "holder_name": row["holder_name"],
                    "languages": row["languages"].split(", ") if row["languages"] else []
                }
                for row in meetings
            ]

            return jsonify({"status": "success", "meetings": meetings_list}), 200
        except Exception as e:
            # 捕獲錯誤並返回錯誤訊息
            return jsonify({"status": "error", "message": str(e)}), 500


# 初始化 DatabaseManager
db_manager = DatabaseManager()

# 創建 ListMeetingAction 實例 
list_meeting_action = ListMeetingAction(db_manager=db_manager)

# 註冊路由
@list_meeting.route('/list-meeting', methods=['GET'])
def list_meeting_route():
    return list_meeting_action.exec()
