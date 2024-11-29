# src/server/main_server.py

import socket
import threading
import os
import sys

# Add the project root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.server.authentication import authenticate_client
from src.server.task_manager import handle_task
from src.utils.logger import log_message

# Server configuration
HOST = '0.0.0.0'  # Bind to all available interfaces
PORT = 9999

def client_handler(client_socket, client_address):
    """
    Handles client connections, authenticates them, and processes their tasks.
    """
    log_message(f"Client {client_address} connected.")
    
    # Authenticate the client
    if authenticate_client(client_socket):
        try:
            # Handle the client's task
            handle_task(client_socket)
        except Exception as e:
            log_message(f"Error handling task for {client_address}: {e}")
        finally:
            client_socket.close()
            log_message(f"Client {client_address} disconnected.")
    else:
        client_socket.close()
        log_message(f"Authentication failed for client {client_address}.")

def main():
    """
    Main function to start the server and handle incoming client connections.
    """
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 pending connections
    log_message(f"Server running on {HOST}:{PORT}")

    try:
        # Accept and handle incoming client connections
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        log_message("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
