import socket

def run_client():
    host = '127.0.0.1'  # Server address
    port = 9999          # Port the server is listening on

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Receive welcome message
        welcome_message = client_socket.recv(1024).decode()
        print(welcome_message)
        
        # Send a task
        client_socket.sendall(b"Test Task")
        
        # Receive the result
        result = client_socket.recv(1024).decode()
        print(result)
        
        # Close the connection
        client_socket.sendall(b"exit")
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_client()
