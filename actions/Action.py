class Action:    
    def __init__(self, name):
        self.name = name
        
    def send_message(self, conn, message):
        conn.send(f"{message}\n".encode('utf-8'))
        
    def get_name(self):
        return self.name
    
    def read_input(self, conn, prompt):
        conn.send(f"[INPUT]{prompt}: ".encode('utf-8'))
        response = conn.recv(1024).decode('utf-8').strip()
        return response
    
    def exec(self, conn, db_manager=None):
        raise NotImplementedError
    
    def validate_input(self, value, max_length, field_name):
        if not value or len(value) > max_length:
            raise ValueError(f"{field_name} must be between 1 and {max_length} characters")
        return value

    def send_table(self, conn, table): 
        conn.sendall(("\n[TABLE]" + '\n' + table + '\n' + "[END]\n").encode('utf-8'))