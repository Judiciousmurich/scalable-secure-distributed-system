import socket
from utils.security import secure_send, secure_receive

HOST = '127.0.0.1'
PORT = 9999

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        secure_send(client_socket, "admin:password")  # Sending credentials
        response = secure_receive(client_socket)
        print(f"Server Response: {response}")

        task = input("Enter a task (e.g., PING or ECHO:<message>): ")
        secure_send(client_socket, task)
        response = secure_receive(client_socket)
        print(f"Server Response: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
