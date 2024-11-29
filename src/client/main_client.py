import socket
import ssl
import json
import threading
from src.client.task_handler import process_task
from src.utils.security import generate_client_credentials

class DistributedTaskClient:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.client_id = generate_client_credentials()
        
    def connect_to_server(self, task):
        try:
            # SSL Context
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((self.host, self.port)) as sock:
                with context.wrap_socket(sock) as secure_sock:
                    # Send authentication
                    self.authenticate(secure_sock)
                    
                    # Send task
                    task_data = json.dumps({
                        'client_id': self.client_id,
                        'task': task
                    })
                    secure_sock.send(task_data.encode('utf-8'))
                    
                    # Receive result
                    result = secure_sock.recv(1024).decode('utf-8')
                    return json.loads(result)
        
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def authenticate(self, socket):
        # Simple authentication mechanism
        auth_data = json.dumps({
            'client_id': self.client_id,
            'auth_token': 'sample_token'
        })
        socket.send(auth_data.encode('utf-8'))

def main():
    client = DistributedTaskClient()
    
    # Example task
    task = {
        'type': 'compute',
        'data': [1, 2, 3, 4, 5],
        'operation': 'sum'
    }
    
    result = client.connect_to_server(task)
    print("Task Result:", result)

if __name__ == "__main__":
    main()