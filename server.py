import socket

HOST = ""  # Localhost
PORT = 12345        # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Listening on {HOST}:{PORT}...")
conn, addr = server.accept()
print(f"Connected by {addr}")

data = conn.recv(1024)  # Receive up to 1024 bytes
print(f"Received: {data.decode()}")

conn.sendall(b"Hello from server!")  # Send a response
conn.close()
