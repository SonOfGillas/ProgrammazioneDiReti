
'''
                        UDP CLIENT SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk
import time
import os
import sys


sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)

 
while True:
    


    getFileList = False;
    reciveFile = False;
    sendFile = False;
     
    filename: str;
    
    while True:
        print("1) get the list of file in the server")
        print("2) get a file from the server")
        print("3) upload a file on the server")
        print("4) exit")
        response = input("Do you want to do?[1/2/3/4] ")
        if response=='1':
            getFileList=True
            break
        elif response=='2':
            reciveFile = True
            filename = input("Insert the name of the file: ")
            break
        elif response=='3':
            sendFile = True
            filename = input("Insert the name of the file: ")
            break
        elif response=='4':
            sock.close()
            sys.exit()
            break
        else :
            print('this is not one of the accetable awnser')
                
    
    try:
        
        if getFileList:
            message='GET list'
            sent = sock.sendto(message.encode(), server_address)
            data, server = sock.recvfrom(4096)
            numberOfFile = int(data.decode('utf8'))
            print("there are '%d' file in the server:" % numberOfFile)
            
            for i in range(0, numberOfFile):
                data, server = sock.recvfrom(4096)
                print(data.decode('utf8'))
                pass
            
        if reciveFile:
            message='Get file'
            sent = sock.sendto(message.encode('utf8'), server_address)
            sent = sock.sendto(filename.encode('utf8'),server_address)
            data, server = sock.recvfrom(4096)
            code=data.decode('utf8').split()[1]
            print(code)
            if code=='202':
                fileFoulder=os.path.join(os.getcwd(),'file')
                filePath=os.path.join(fileFoulder,filename)
                newFile = open(filePath, 'w')
                data, server = sock.recvfrom(4096)
                newFile.write(data.decode('utf8'))
    
        if sendFile:
            message='POST'
            sent = sock.sendto(message.encode('utf8'), server_address)
            f = open(filename,'r+')
            outputdata = f.read()
            print ('sending "%s"' % f.name)
            sent = sock.sendto(f.name.encode('utf8'),server_address)
            sent = sock.sendto(outputdata.encode('utf8'), server_address)
            
        print('\n\n')
    
    except Exception as info:
        print(info)
        sock.close()
        
