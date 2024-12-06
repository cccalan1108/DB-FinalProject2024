
class Action:    
    def __init__(self, action_name):
        self.action_name = action_name
        
    def exec(self, conn, db_manager=None, **kwargs):
        raise NotImplementedError
        
    def get_name(self):
        return self.action_name
    
    def read_input(self, conn, prompt):
        conn.send(f'[INPUT]{prompt}: '.encode('utf-8'))
        return conn.recv(1024).decode('utf-8').strip()
    
    def send_message(self, conn, message):
        conn.send(f"{message}\n".encode('utf-8'))

    def validate_input(self, value, max_length, field_name):
        if not value or len(value) > max_length:
            raise ValueError(f"{field_name} must be between 1 and {max_length} characters")
        return value
    
    def send_table(self, conn, table): 
        conn.sendall(("[TABLE]" + '\n' + table + '\n' + "[END]").encode('utf-8'))