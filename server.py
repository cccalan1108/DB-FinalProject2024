import socket
from threading import Thread
from config import Config
from DB_utils import DatabaseManager
from role.User import User
from role.Admin import Admin
from role.Visitor import Visitor
from datetime import datetime

class Server:
    def __init__(self):
        self.config = Config
        self.host = self.config.SERVER_HOST
        self.port = self.config.SERVER_PORT
        self.server_socket = None
        self.db_manager = DatabaseManager()
        self.clients = {}
        
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
                
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        try:
            user = None
            print(f"New client connected: {client_address}")
            
            while True:
                if user is None:
                    current_actions = Visitor().get_visitor_actions()
                    for action in current_actions:
                        action.server = self
                else:
                    current_actions = user.get_actions()
                    for action in current_actions:
                        action.server = self
                    self.clients[user.get_userid()] = client_socket
                
                menu = self._create_menu(current_actions)
                client_socket.send(menu.encode('utf-8'))
                choice = self._receive_input(client_socket)
                
                if not choice.isdigit() or int(choice) not in range(1, len(current_actions) + 1):
                    client_socket.send("Invalid option! Please try again.\n".encode('utf-8'))
                    continue
                
                action = current_actions[int(choice) - 1]
                if user is None:
                    result = action.exec(client_socket, self.db_manager)
                else:
                    result = action.exec(client_socket, self.db_manager, user=user)
                
                if isinstance(result, str):
                    if result == "exit":
                        print(f"Client {client_address} requested to exit")
                        break
                    elif result == "logout":
                        user = None
                        continue
                elif isinstance(result, (User, Admin)):
                    user = result
                    
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
    
    def _receive_input(self, client_socket):
        try:
            return client_socket.recv(1024).decode('utf-8').strip()
        except:
            return ""
            
    def _create_menu(self, actions):
        menu = "="*26
        menu += "\nAvailable actions:"
        for i, action in enumerate(actions, 1):
            menu += f"\n{i}. {action.get_name()}"
        menu += "\n[INPUT]Please choose an action: "
        return menu
    
    def broadcast_message(self, receiver_id, message):
        if receiver_id in self.clients:
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                formatted_message = f"[{timestamp}] {message}"
                self.clients[receiver_id].send(f"[CHAT]{formatted_message}".encode('utf-8'))
            except:
                pass

if __name__ == "__main__":
    server = Server()
    server.start()