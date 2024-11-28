import socket
import threading
from authentication import authenticate_client
from task_manager import handle_task
from utils.logger import log_message

HOST = '0.0.0.0'  # Bind to all available interfaces
PORT = 9999

def client_handler(client_socket, client_address):
    log_message(f"Client {client_address} connected.")
    if authenticate_client(client_socket):
        try:
            handle_task(client_socket)
        except Exception as e:
            log_message(f"Error handling task: {e}")
        finally:
            client_socket.close()
            log_message(f"Client {client_address} disconnected.")
    else:
        client_socket.close()
        log_message(f"Authentication failed for {client_address}.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    log_message(f"Server running on {HOST}:{PORT}")

    try:
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
