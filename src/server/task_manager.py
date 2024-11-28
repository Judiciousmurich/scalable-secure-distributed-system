def handle_task(client_socket):
    task_request = client_socket.recv(1024).decode()
    if task_request == "PING":
        client_socket.send("PONG".encode())
    elif task_request.startswith("ECHO:"):
        message = task_request[5:]
        client_socket.send(f"ECHOING: {message}".encode())
    else:
        client_socket.send("UNKNOWN TASK".encode())
