import socket
from config import Config
from threading import Thread

class Client:
    def __init__(self):
        self.config = Config()
        self.host = self.config.SERVER_HOST  
        self.port = self.config.SERVER_PORT
        self.client_socket = None
        self.is_chatting = False
        self.last_input_prompt = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def handle_message(self, message: str) -> None:
        if not message.strip():
            return
            
        if message.startswith('['):
            self._handle_tagged_message(message)
            return
        
        if message.startswith('==='):
            print(f"\n{message}")
        elif message.startswith(tuple('0123456789')):
            print(message)
        else:
            print(message)

    def _handle_tagged_message(self, message: str) -> None:
        if "[TABLE]" in message:
            print()
            return
            
        if "[END]" in message:
            print()
            return
            
        if "[CHAT_START]" in message:
            self.is_chatting = True
            print("\nMessage: ", end='')
            return
            
        if "[CHAT_END]" in message:
            self.is_chatting = False
            print()
            return
            
        if "[INPUT]" in message:
            prompt = message.replace("[INPUT]", "")
            if prompt != self.last_input_prompt:
                if ("action" in prompt.lower() or 
                    "option" in prompt.lower() or 
                    "choice" in prompt.lower() or
                    "select" in prompt.lower()):
                    print(f"\n{prompt}", end='')
                else:
                    print(f"\r{prompt}", end='')
                self.last_input_prompt = prompt
            return
            
        if "[CHAT]" in message:
            chat_msg = message.replace("[CHAT]", "")
            if "[INPUT]Message:" not in chat_msg:
                current_prompt = self.last_input_prompt
                print('\r' + ' ' * 100 + '\r', end='')
                print(f"{chat_msg}")
                if self.is_chatting and "Message sent!" not in chat_msg:
                    print("Message: ", end='', flush=True)
                elif not self.is_chatting and current_prompt:
                    print(f"{current_prompt}", end='', flush=True)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                        
                for message in data.split('\n'):
                    self.handle_message(message)
                    
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    def start(self):
        if not self.connect():
            return
            
        try:
            receive_thread = Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self._handle_user_input()
                
        except KeyboardInterrupt:
            print("\nClosing connection...")
        finally:
            self.close()

    def _handle_user_input(self):
        while True:
            try:
                if not self.is_chatting:
                    user_input = input()
                else:
                    user_input = input("Message: ")
                 
                if user_input.lower() == 'exit':
                    if self.is_chatting:
                        self.is_chatting = False
                    else:
                        break
                        
                self.client_socket.send(user_input.encode('utf-8'))
                self.last_input_prompt = None
                
            except EOFError:
                break

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client = Client()
    client.start()
