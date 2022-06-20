'''
                            UDP SERVER SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk
import time
import os


# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    print('\n\r waiting to receive message...')
    
    data, address = sock.recvfrom(4096)
    request = data.decode('utf8')
    print (request)

    try:
        if request == 'POST': 
            data, address = sock.recvfrom(4096)
            print (data.decode('utf8'))
            filePath=os.path.join(os.getcwd(), data.decode('utf8'))
            file = open(filePath, 'w')
            data, address = sock.recvfrom(4096)
            print (data.decode('utf8'))
            file.write(data.decode('utf8'))
    
            
        elif request == 'GET list':
            filePath=os.path.join(os.getcwd(), 'file')
            serverFileList=os.listdir(filePath)
            numberOfFile=len(serverFileList)
            sent = sock.sendto(str(numberOfFile).encode('utf8'), address)
            
            for i in range(0, numberOfFile):
                sent = sock.sendto(serverFileList[i].encode('utf8'), address)
                pass
            
        elif request == 'Get file':
            data, address = sock.recvfrom(4096)
            print (data.decode('utf8'))
            fileFoulder = os.path.join(os.getcwd(), 'file')
            filePath = os.path.join(fileFoulder, data.decode('utf8'))
            
            if os.path.exists(filePath):
                serverResponse='HTTP/1.1 202 File Found'
                sent = sock.sendto(serverResponse.encode(), address)
                f = open(filePath,'r+')
                fileContent = f.read()
                sent = sock.sendto(fileContent.encode('utf8'), address)
            else :
                serverResponse='HTTP/1.1 404 File Not Found\r\n\r\n'
                sent = sock.sendto(serverResponse.encode(), address)
            
        else :
            serverResponse='HTTP/1.1 404 Unknown Request\r\n\r\n'
            sent = sock.sendto(serverResponse.encode(), address)
            
    except Exception as info:
        serverResponse='HTTP/1.1 505 Internal Server Error\r\n\r\n'
        sent = sock.sendto(serverResponse.encode(), address)
        sock.close()        
