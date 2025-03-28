import socket

HOST = ""  # Server IP (localhost in this case)
PORT = 12345        # Port to connect to

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.sendall(b"Hello from client!")  # Send a message

data = client.recv(1024)  # Receive the response
print(f"Received: {data.decode()}")

client.close()
