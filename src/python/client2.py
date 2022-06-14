from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost',10000))

full_msg=''

while True:
    msg = clientSocket.recv(5)
    if len(msg) <= 0:
        break
    full_msg += msg.decode()
    
print(full_msg)
