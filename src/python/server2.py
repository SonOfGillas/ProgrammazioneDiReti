from socket import * 

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('',10000))

serverSocket.listen(5)

while True:
    clientsocket,address = serverSocket.accept()
    print(f"conncetion from {address} has benne enstablished")
    message="Hello World!"
    clientsocket.send(message.encode())
    clientsocket.close()