def authenticate_client(client_socket):
    client_socket.send("AUTH".encode())
    credentials = client_socket.recv(1024).decode()
    username, password = credentials.split(":")
    return username == "admin" and password == "password"
