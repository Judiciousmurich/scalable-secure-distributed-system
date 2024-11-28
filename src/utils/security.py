def secure_send(sock, data):
    sock.send(data.encode())

def secure_receive(sock):
    return sock.recv(1024).decode()
