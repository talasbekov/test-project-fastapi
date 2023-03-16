import os
import socket
import time

# Set up socket
HOST = ''  # Listen on all available interfaces
PORT = 5000  # Port number to listen on
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Accept a client connection
conn, addr = sock.accept()
print(f'Connected by {addr}')
