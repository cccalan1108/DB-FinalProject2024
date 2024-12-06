import socket
from config import Config

class Client:
    def __init__(self):
        self.config = Config
        self.host = self.config.SERVER_HOST
        self.port = self.config.SERVER_PORT
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def receive_message(self):
        try:
            message = b""
            first_chunk = self.client_socket.recv(4096)
            if "[TABLE]".encode('utf-8') not in first_chunk:
                return first_chunk.decode('utf-8')
            
            message += first_chunk

            while True:
                chunk = self.client_socket.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection lost while receiving data")
                message += chunk
                if "[END]".encode('utf-8') in message:
                    break
            return message.decode('utf-8').replace("[END]", '').replace("[TABLE]", '')
        except Exception as e:
            print(f"Receive message error:{e}.")
            return None

    def start(self):
        if self.connect():
            try:
                while True:
                    message = self.receive_message()
                    if not message:
                        break

                    if "[INPUT]" in message:
                        prompt = message.replace("[INPUT]", "")
                        print(prompt, end='')
                        
                        user_input = input()
                        
                        if user_input.lower() == 'exit':
                            break
                            
                        self.client_socket.send(user_input.encode('utf-8'))
                    else:
                        print(message)

            except ConnectionError:
                print("Lost connection to server")
            except KeyboardInterrupt:
                print("\nClient shutting down...")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.close()
                
    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client = Client()
    client.start()