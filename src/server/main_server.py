import socket
import threading
import ssl
import json
import logging
from src.utils.logger import setup_logging
from src.server.authentication import authenticate_client
from src.server.task_manager import TaskManager

class DistributedTaskServer:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.task_manager = TaskManager()
        self.logger = setup_logging('server')
        
        # SSL Context Setup
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        
    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            self.logger.info(f"Server listening on {self.host}:{self.port}")
            
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(server_socket, server_side=True)
            
            while True:
                try:
                    client_socket, address = secure_socket.accept()
                    self.logger.info(f"Connection from {address}")
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket,)
                    )
                    client_thread.start()
                    
                except Exception as e:
                    self.logger.error(f"Server error: {e}")
    
    def handle_client(self, client_socket):
        try:
            # Authenticate client
            if not authenticate_client(client_socket):
                client_socket.close()
                return
            
            # Receive task
            data = client_socket.recv(1024).decode('utf-8')
            task = json.loads(data)
            
            # Process task
            result = self.task_manager.execute_task(task)
            
            # Send result back
            client_socket.send(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.logger.error(f"Client handling error: {e}")
        finally:
            client_socket.close()

def main():
    server = DistributedTaskServer()
    server.start_server()

if __name__ == "__main__":
    main()