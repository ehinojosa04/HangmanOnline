import socket

UDP_IP = "127.0.0.1"  # Server IP
UDP_PORT = 5001  # Listening on PORT+1 as per your server

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP messages on {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(2044)  # Buffer size is 1024 bytes
    data = data.strip()
    print(f"Received message from {addr}: {data.decode(encoding='windows-1252')}")

