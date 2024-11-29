from src.utils.logger import log_info, log_error

import socket
import threading
import os
import sys

# Add the project root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.server.task_manager import handle_task
from src.utils.logger import setup_logging

# Set up a logger specifically for the main server
logger = setup_logging("main_server")

HOST = '0.0.0.0'  # Bind to all available interfaces
PORT = 9999

def client_handler(client_socket, client_address):
    log_info(logger, f"Client {client_address} connected.")
    try:
        handle_task(client_socket, client_address)
    except Exception as e:
        log_error(logger, f"Error handling task for {client_address}", e)
    finally:
        client_socket.close()
        log_info(logger, f"Client {client_address} disconnected.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    log_info(logger, f"Server running on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        log_info(logger, "Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
