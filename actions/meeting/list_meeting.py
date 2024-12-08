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

from flask import Blueprint, jsonify, render_template
from datetime import date, time, datetime
from DB_utils import DatabaseManager

list_meeting = Blueprint("list_meeting", __name__)

class ListMeetingAction:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def exec(self):
        try:
            meetings = self.db_manager.get_all_meetings()
            if not meetings:
                return jsonify({"status": "error", "message": "No available meetings found"}), 404

            meetings_list = []
            for row in meetings:
                meeting = {
                    "meeting_id": row["meeting_id"],
                    "content": row["content"],
                    "event_date": row["event_date"].strftime("%a, %d %b %Y") if isinstance(row["event_date"], (date, datetime)) else row["event_date"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "event_city": row["event_city"],
                    "event_place": row["event_place"],
                    "status": row["status"],
                    "num_participant": row["num_participant"],
                    "max_participant": row["max_participant"],
                    "holder_name": row["holder_name"],
                    "languages": [lang.encode('latin1').decode('utf-8') for lang in row["languages"]] if row["languages"] else []
                }
                meetings_list.append(meeting)

            return jsonify({"status": "success", "meetings": meetings_list}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500



# 初始化 DatabaseManager
db_manager = DatabaseManager()

# 創建 ListMeetingAction 實例 
list_meeting_action = ListMeetingAction(db_manager=db_manager)


# @list_meeting.route('/list_meeting', methods=['GET'])
# def list_meeting_route():
#     response = list_meeting_action.exec()
#     print("Data returned to frontend:", response)
#     return response


@list_meeting.route('/list_meeting', methods=['GET'])
def list_meeting_route():
    # 直接渲染 HTML 頁面，數據通過前端 fetch 獲取
    return render_template('list_meeting.html')

@list_meeting.route('/list_meeting_data', methods=['GET'])
def list_meeting_data():
    return list_meeting_action.exec()  # 仍然返回 JSON 數據


@list_meeting.route('/join_meeting/<int:meeting_id>', methods=['POST'])
def join_meeting(meeting_id):
    try:
        # 在這裡加入邏輯，確認使用者可以加入會議，並更新資料庫
        # 例如：檢查會議是否存在，參與人數是否已滿等
        meeting = db_manager.get_meeting_by_id(meeting_id)
        if not meeting:
            return jsonify({"status": "error", "message": "Meeting not found"}), 404

        if meeting["num_participant"] >= meeting["max_participant"]:
            return jsonify({"status": "error", "message": "Meeting is full"}), 400

        # 加入會議邏輯（例如，更新 num_participant）
        db_manager.join_meeting(meeting_id)  # 實現這個函數來更新資料庫

        return jsonify({"status": "success", "message": f"Joined meeting {meeting_id} successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
