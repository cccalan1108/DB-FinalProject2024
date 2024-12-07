import psycopg2
from config import Config
from tabulate import tabulate
from datetime import datetime
from flask import jsonify

class DatabaseManager:
    def __init__(self):
        self.config = Config
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                host=self.config.DB_HOST,
                port=self.config.DB_PORT
            )
            self.cursor = self.connection.cursor()

        except psycopg2.Error as e:
            self.connection = None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except psycopg2.Error as e:
            print(f"Query execution error: {e}")
            self.connection.rollback()
            return None

        
    def print_table(self, cur):
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        return tabulate(rows, headers=columns, tablefmt="github")

    def check_account_exists(self, account):

        query = 'SELECT COUNT(*) FROM "USER" WHERE Account = %s'
        result = self.execute_query(query, (account,))
        return result[0][0] > 0 if result else False

    def create_user(self, **user_data):
        try:
            query = 'SELECT COALESCE(MAX(User_id), 0) + 1 FROM "USER"'
            result = self.execute_query(query)
            if not result:
                return False
            user_id = result[0][0]

            insertUser_query =  """
                            INSERT INTO "USER" (
                                User_id, Account, User_name, User_nickname, Password, 
                                Nationality, City, Phone, Email, Sex, Birthday, Register_time
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            )
                            """
            
            success = self.execute_query(insertUser_query, (
                user_id,
                user_data['account'],
                user_data['user_name'],
                user_data['user_nickname'],
                user_data['password'],
                user_data['nationality'],
                user_data['city'],
                user_data['phone'],
                user_data['email'],
                user_data['sex'],
                user_data['birthday'],
                user_data['register_time']
            ))

            if user_data['admin_code'] == 123456:
                if not success:
                    return False
                
                Role = 'Admin'
                insertUserDetail_query =  'INSERT INTO "user_role" (User_id, Role) VALUES (%s, %s)'     
                return self.execute_query(insertUserDetail_query, (user_id, Role))
                
            else:
                if not success:
                    return False
                
                insertUserDetail_query = 'INSERT INTO "user_role" (User_id, Role) VALUES (%s, %s)'
                return self.execute_query(insertUserDetail_query, (user_id, 'User'))
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def verify_login(self, account, password):
        query = """
                SELECT u.User_id, u.User_name, u.User_nickname, u.Email, r.Role
                FROM "USER" u
                JOIN "user_role" r ON u.User_id = r.User_id
                WHERE u.Account = %s AND u.Password = %s
                """
        result = self.execute_query(query, (account, password))
        
        # 登入成功
        if result and len(result) > 0:
            row = result[0]
            response = {
                "status": "success",
                "message": f"Welcome back, {row[1]}!",
                "user_id": row[0],
                "role": row[4],
                'email': row[3],
                'nickname': row[2],
                'user_name': row[1]
            }
            return jsonify(response)
        
        # 登入失敗
        response = {
            "status": "error",
            "message": "Invalid account or password!"
        }
        return jsonify(response)
    
    def get_private_messages(self, sender_id, receiver_id, limit=10):
        query = """
                SELECT pm.Sender_id, pm.Content, pm.Sending_time, u.User_nickname
                FROM PRIVATE_MESSAGE pm
                JOIN "USER" u ON pm.Sender_id = u.User_id
                WHERE (pm.Sender_id = %s AND pm.Receiver_id = %s)
                OR (pm.Sender_id = %s AND pm.Receiver_id = %s)
                ORDER BY pm.Sending_time DESC
                LIMIT %s
                """
        result = self.execute_query(query, (sender_id, receiver_id, receiver_id, sender_id, limit))
        if result:
            messages = list(reversed(result))
            return messages
        return []
    def get_meeting_messages(self, meeting_id, limit=10):
        query = """
                SELECT cr.Sender_id, cr.Content, cr.Sending_time, u.User_nickname
                FROM CHATTING_ROOM cr
                JOIN "USER" u ON cr.Sender_id = u.User_id
                WHERE cr.Meeting_id = %s
                ORDER BY cr.Sending_time DESC
                LIMIT %s
                """
        result = self.execute_query(query, (meeting_id, limit))
        if result:
            messages = list(reversed(result))[-limit:]
            return messages
        return []

    def send_private_message(self, sender_id, receiver_id, content):
        query = """
                INSERT INTO PRIVATE_MESSAGE (Sender_id, Receiver_id, Sending_time, Content)
                VALUES (%s, %s, NOW(), %s)
                """
        return self.execute_query(query, (sender_id, receiver_id, content))

    def send_meeting_message(self, meeting_id, sender_id, content):
        try:
            query = """
                    INSERT INTO CHATTING_ROOM (Meeting_id, Sender_id, Sending_time, Content)
                    VALUES (%s, %s, NOW(), %s)
                    """
            return self.execute_query(query, (meeting_id, sender_id, content))
        except Exception as e:
            print(f"Error sending meeting message: {e}")
            return False
    
    def update_user_detail(self, field, value, user_id):
        try:
            query = f"""
                    INSERT INTO USER_DETAIL (User_id, {field})
                    VALUES (%s, %s)
                    ON CONFLICT (User_id) 
                    DO UPDATE SET {field} = EXCLUDED.{field}
                    """
            return self.execute_query(query, (user_id, value))
        except Exception as e:
            print(f"Error updating user detail: {e}")
            return False
    
    def get_all_meetings(self):
        query = """
                SELECT 
                    m.Meeting_id,
                    m.Content,
                    m.Event_date,
                    m.Start_time,
                    m.End_time,
                    m.Event_city,
                    m.Event_place,
                    m.Status,
                    m.Num_participant,
                    m.Max_num_participant,
                    u.User_name as holder_name,
                    string_agg(ml.Language, ', ') as languages
                FROM MEETING m
                JOIN "USER" u ON m.Holder_id = u.User_id
                LEFT JOIN MEETING_LANGUAGE ml ON m.Meeting_id = ml.Meeting_id
                WHERE m.Status = 'Ongoing'
                GROUP BY m.Meeting_id, m.Content, m.Event_date, m.Start_time, m.End_time,
                        m.Event_city, m.Event_place, m.Status, m.Num_participant, 
                        m.Max_num_participant, u.User_name
                ORDER BY m.Event_date, m.Start_time
                """
        self.cursor.execute(query)
        return self.print_table(self.cursor)

    def create_meeting(self, holder_id, content, event_date, start_time, end_time, 
                  event_city, event_place, max_participants, languages):
        try:
            query = "SELECT COALESCE(MAX(Meeting_id), 0) + 1 FROM MEETING"
            result = self.execute_query(query)
            meeting_id = result[0][0]
            
            query = """
                    INSERT INTO MEETING (
                        Meeting_id, Holder_id, Content, Event_date, Start_time, End_time,
                        Event_city, Event_place, Status, Num_participant, Max_num_participant
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Ongoing', 1, %s)
                    """
            self.execute_query(query, (
                meeting_id, holder_id, content, event_date, start_time, end_time,
                event_city, event_place, max_participants
            ))
            
            for lang in languages:
                query = "INSERT INTO MEETING_LANGUAGE (Meeting_id, Language) VALUES (%s, %s)"
                self.execute_query(query, (meeting_id, lang))
                
            query = """
                    INSERT INTO PARTICIPATION (User_id, Meeting_id, Join_time)
                    VALUES (%s, %s, NOW())
                    """
            self.execute_query(query, (holder_id, meeting_id))
            
            return meeting_id
            
        except Exception as e:
            print(f"Error creating meeting: {e}")
            return None

    def check_meeting_availability(self, meeting_id):
        query = """
                SELECT Meeting_id 
                FROM MEETING 
                WHERE Meeting_id = %s 
                AND Status = 'Ongoing'
                AND Num_participant < Max_num_participant
                """
        result = self.execute_query(query, (meeting_id,))
        return result and len(result) > 0
    
    def is_user_in_meeting(self, user_id, meeting_id):
        query = """
                SELECT 1
                FROM participation
                WHERE User_id = %s AND Meeting_id = %s
                """
        result = self.execute_query(query, (user_id, meeting_id))
        return bool(result)
    
    def join_meeting(self, user_id, meeting_id):
        try:
            query1 = """
                    INSERT INTO PARTICIPATION (User_id, Meeting_id, Join_time)
                    VALUES (%s, %s, NOW())
                    """
            self.execute_query(query1, (user_id, meeting_id))
            
            query2 = """
                    UPDATE MEETING 
                    SET Num_participant = Num_participant + 1
                    WHERE Meeting_id = %s
                    """
            self.execute_query(query2, (meeting_id,))
            
            return True
        except Exception as e:
            print(f"Error joining meeting: {e}")
            return False
    def get_user_meetings(self, user_id):
        query = """
                SELECT m.Meeting_id, m.Content, m.Event_city, m.Event_place, 
                       m.Event_date, m.Start_time, m.End_time, m.Holder_id,
                       m.Max_num_participant,
                       (SELECT COUNT(*) FROM participation p2 WHERE p2.Meeting_id = m.Meeting_id) as num_participant
                FROM MEETING m
                JOIN participation p ON m.Meeting_id = p.Meeting_id
                WHERE p.User_id = %s AND m.Status = 'Ongoing'
                """
        result = self.execute_query(query, (user_id,))
        if result:
            return [
                {
                    'meeting_id': row[0],
                    'content': row[1],
                    'event_city': row[2],
                    'event_place': row[3],
                    'event_date': row[4],
                    'start_time': row[5],
                    'end_time': row[6],
                    'holder_id': row[7],
                    'max_participant': row[8],
                    'num_participant': row[9]
                }
                for row in result
            ]
        return []

    def leave_meeting(self, user_id, meeting_id):
        try:
            query1 = """
                    DELETE FROM PARTICIPATION 
                    WHERE User_id = %s AND Meeting_id = %s
                    """
            self.execute_query(query1, (user_id, meeting_id))
            
            query2 = """
                    UPDATE MEETING 
                    SET Num_participant = Num_participant - 1
                    WHERE Meeting_id = %s
                    """
            self.execute_query(query2, (meeting_id,))
            
            return True
        except Exception as e:
            print(f"Error leaving meeting: {e}")
            return False
    def get_hosted_meetings(self, user_id):
        query = """
                SELECT 
                    m.Meeting_id,
                    m.Content,
                    m.Event_date,
                    m.Event_place,
                    m.Num_participant,
                    m.Max_num_participant
                FROM MEETING m
                WHERE m.Holder_id = %s 
                AND m.Status = 'Ongoing'
                ORDER BY m.Event_date, m.Start_time
                """
        result = self.execute_query(query, (user_id,))
        if not result:
            return []
            
        meetings = []
        for row in result:
            meetings.append({
                'meeting_id': row[0],
                'content': row[1],
                'event_date': row[2],
                'event_place': row[3],
                'num_participant': row[4],
                'max_participant': row[5]
            })
        return meetings

    def cancel_meeting(self, meeting_id):
        try:
            query = """
                    UPDATE MEETING 
                    SET Status = 'Canceled'
                    WHERE Meeting_id = %s
                    """
            self.execute_query(query, (meeting_id,))
            
            return True
        except Exception as e:
            print(f"Error canceling meeting: {e}")
            return False
        
    def finish_meeting(self, meeting_id):
        try:
            query = """
                    UPDATE MEETING 
                    SET Status = 'Finished'
                    WHERE Meeting_id = %s
                    AND Status = 'Ongoing'
                    """
            self.execute_query(query, (meeting_id,))
            return True
        except Exception as e:
            print(f"Error finishing meeting: {e}")
            return False
        
    def get_user_meeting_history(self, user_id):
        query = """
                SELECT 
                    m.Meeting_id,
                    m.Content,
                    m.Event_date,
                    m.Start_time,
                    m.End_time,
                    m.Event_city,
                    m.Event_place,
                    m.Status,
                    m.Num_participant,
                    m.Max_num_participant,
                    string_agg(ml.Language, ', ') as languages,
                    CASE 
                        WHEN m.Holder_id = %s THEN 'Host'
                        ELSE 'Participant'
                    END as role
                FROM MEETING m
                JOIN PARTICIPATION p ON m.Meeting_id = p.Meeting_id
                LEFT JOIN MEETING_LANGUAGE ml ON m.Meeting_id = ml.Meeting_id
                WHERE p.User_id = %s
                GROUP BY m.Meeting_id, m.Content, m.Event_date, m.Start_time, m.End_time,
                        m.Event_city, m.Event_place, m.Status, m.Num_participant, 
                        m.Max_num_participant, m.Holder_id
                ORDER BY m.Event_date DESC, m.Start_time DESC
                """
        self.cursor.execute(query, (user_id, user_id))
        return self.print_table(self.cursor)

    def get_all_meetings_admin(self):
        query = """
                SELECT 
                    m.Meeting_id,
                    m.Content,
                    m.Event_date,
                    m.Start_time,
                    m.End_time,
                    m.Event_city,
                    m.Event_place,
                    m.Status,
                    m.Num_participant,
                    m.Max_num_participant,
                    u.User_name as holder_name,
                    string_agg(ml.Language, ', ') as languages
                FROM MEETING m
                JOIN "USER" u ON m.Holder_id = u.User_id
                LEFT JOIN MEETING_LANGUAGE ml ON m.Meeting_id = ml.Meeting_id
                GROUP BY 
                    m.Meeting_id, m.Content, m.Event_date, m.Start_time,
                    m.End_time, m.Event_city, m.Event_place, m.Status,
                    m.Num_participant, m.Max_num_participant, u.User_name
                ORDER BY m.Event_date DESC, m.Start_time DESC
                """
        self.cursor.execute(query)
        return self.print_table(self.cursor)

    def admin_cancel_meeting(self, meeting_id):
        try:
            query = """
                    UPDATE MEETING 
                    SET Status = 'Canceled'
                    WHERE Meeting_id = %s
                    AND Status = 'Ongoing'
                    """
            self.execute_query(query, (meeting_id,))
            return True
        except Exception as e:
            print(f"Error in admin cancel meeting: {e}")
            return False

    def admin_finish_meeting(self, meeting_id):
        try:
            query = """
                    UPDATE MEETING 
                    SET Status = 'Finished'
                    WHERE Meeting_id = %s
                    AND Status = 'Ongoing'
                    """
            self.execute_query(query, (meeting_id,))
            return True
        except Exception as e:
            print(f"Error in admin finish meeting: {e}")
            return False
    
    def get_user_info(self, user_id):
        query = """
                SELECT 
                    u.User_id,
                    u.User_name,
                    u.User_nickname,
                    u.Nationality,
                    u.City,
                    u.Email,
                    ud.Star_sign,
                    ud.Mbti,
                    ud.Blood_type,
                    ud.Religion,
                    ud.University,
                    ud.Married,
                    ud.Sns,
                    ud.Self_introduction,
                    ud.Interest,
                    ud.Find_meeting_type
                FROM "USER" u
                LEFT JOIN USER_DETAIL ud ON u.User_id = ud.User_id
                WHERE u.User_id = %s
                """
        self.cursor.execute(query, (user_id,))
        return self.print_table(self.cursor)

    def add_sns_detail(self, user_id, sns_type, sns_id):
        try:
            query = """
                    INSERT INTO SNS_DETAIL (User_id, Sns_type, Sns_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (User_id, Sns_type) 
                    DO UPDATE SET Sns_id = EXCLUDED.Sns_id
                    """
            return self.execute_query(query, (user_id, sns_type, sns_id))
        except Exception as e:
            print(f"Error adding SNS detail: {e}")
            return False

    def get_user_nickname(self, user_id):
        query = """
                SELECT User_nickname
                FROM "USER"
                WHERE User_id = %s
                """
        result = self.execute_query(query, (user_id,))
        return result[0][0] if result else None

    def get_meeting_participants(self, meeting_id):
        query = """
                SELECT User_id
                FROM participation
                WHERE Meeting_id = %s
                """
        result = self.execute_query(query, (meeting_id,))
        return [row[0] for row in result] if result else []

    def get_private_chat_history(self, user_id, partner_id):
        query = """
                SELECT 
                    CASE WHEN pm.Sender_id = %s THEN 'You' ELSE u.User_nickname END as sender,
                    pm.Content as message,
                    pm.Sending_time as time
                FROM PRIVATE_MESSAGE pm
                JOIN "USER" u ON pm.Sender_id = u.User_id
                WHERE (pm.Sender_id = %s AND pm.Receiver_id = %s)
                OR (pm.Sender_id = %s AND pm.Receiver_id = %s)
                ORDER BY pm.Sending_time
                """
        self.cursor.execute(query, (user_id, user_id, partner_id, partner_id, user_id))
        return self.print_table(self.cursor)

    def get_meeting_chat_history(self, meeting_id):
        query = """
                SELECT 
                    u.User_nickname as sender,
                    cr.Content as message,
                    cr.Sending_time as time
                FROM CHATTING_ROOM cr
                JOIN "USER" u ON cr.Sender_id = u.User_id
                WHERE cr.Meeting_id = %s
                ORDER BY cr.Sending_time
                """
        self.cursor.execute(query, (meeting_id,))
        return self.print_table(self.cursor)

    def get_all_non_admin_users(self):
        query = """
                SELECT DISTINCT
                    u.User_id,
                    u.User_name,
                    u.User_nickname,
                    u.Nationality,
                    u.City,
                    u.Email
                FROM "USER" u
                LEFT JOIN USER_ROLE ur ON u.User_id = ur.User_id AND ur.Role = 'Admin'
                WHERE ur.User_id IS NULL
                ORDER BY u.User_id
                """
        self.cursor.execute(query)
        return self.print_table(self.cursor)

    def get_user_chat_records(self, user_id):
        query = """
                SELECT DISTINCT 
                    CASE 
                        WHEN pm.Sender_id = %s THEN pm.Receiver_id
                        ELSE pm.Sender_id 
                    END as chat_id,
                    u.User_nickname as chat_name,
                    MAX(pm.Sending_time) as last_chat_time
                FROM PRIVATE_MESSAGE pm
                JOIN "USER" u ON (
                    CASE 
                        WHEN pm.Sender_id = %s THEN pm.Receiver_id
                        ELSE pm.Sender_id 
                    END = u.User_id
                )
                WHERE pm.Sender_id = %s OR pm.Receiver_id = %s
                GROUP BY 
                    CASE 
                        WHEN pm.Sender_id = %s THEN pm.Receiver_id
                        ELSE pm.Sender_id 
                    END,
                    u.User_nickname
                ORDER BY last_chat_time DESC
                """
        result = self.execute_query(query, (user_id, user_id, user_id, user_id, user_id))
        if not result:
            return []
        
        chat_records = []
        for row in result:
            chat_records.append({
                'chat_id': row[0],
                'chat_name': row[1],
                'last_time': row[2]
            })
        return chat_records

    def get_chat_history(self, user_id, chat_id):
        query = """
                SELECT 
                    CASE WHEN pm.Sender_id = %s THEN 'You' ELSE u.User_nickname END as sender,
                    pm.Content as message,
                    pm.Sending_time as time
                FROM PRIVATE_MESSAGE pm
                JOIN "USER" u ON pm.Sender_id = u.User_id
                WHERE (pm.Sender_id = %s AND pm.Receiver_id = %s)
                OR (pm.Sender_id = %s AND pm.Receiver_id = %s)
                ORDER BY pm.Sending_time
                """
        self.cursor.execute(query, (user_id, user_id, chat_id, chat_id, user_id))
        return self.print_table(self.cursor)

    def is_admin(self, user_id):
        query = """
                SELECT COUNT(*) 
                FROM user_role 
                WHERE User_id = %s AND Role = 'Admin'
                """
        result = self.execute_query(query, (user_id,))
        return result[0][0] > 0 if result else False

    def get_available_users(self, current_user_id):
        query = """
            SELECT u.User_id, u.User_nickname as nickname
            FROM "USER" u
            LEFT JOIN user_role ur ON u.User_id = ur.User_id AND ur.Role = 'Admin'
            WHERE u.User_id != %s AND ur.User_id IS NULL
            ORDER BY u.User_nickname
        """
        result = self.execute_query(query, (current_user_id,))
        if not result:
            return []
        
        users = []
        for row in result:
            users.append({
                'user_id': row[0],
                'nickname': row[1]
            })
        return users
