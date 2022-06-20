import socket as sk
import os
import sys


sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)


def checkEndingMessage(data):
  response=data.decode('utf8').split();
  isEnding = response[len(response)-1]=='\r\n\r\n'
  if isEnding:
      code = response[1]
      message = response[2]
      print(code, message)
  return isEnding
 
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
            filename = input("Insert the name of the file (es ./file/client_file_1.txt): ")
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
            if checkEndingMessage(data):
                continue
            else :
                numberOfFile = int(data.decode('utf8'))
                print("there are '%d' file in the server:" % numberOfFile)
            
            for i in range(0, numberOfFile):
                data, server = sock.recvfrom(4096)
                if checkEndingMessage(data):
                    break
                else :
                    print(data.decode('utf8'))
                pass
            
            data, server = sock.recvfrom(4096)
            if checkEndingMessage(data):
                continue
            
        if reciveFile:
            message='Get file'
            sent = sock.sendto(message.encode('utf8'), server_address)
            sent = sock.sendto(filename.encode('utf8'),server_address)
            data, server = sock.recvfrom(4096)
            code=data.decode('utf8').split()[1]
            if code=='202':
                print('start file download...')
                fileFoulder=os.path.join(os.getcwd(),'file')
                filePath=os.path.join(fileFoulder,filename)
                newFile = open(filePath, 'w')
                data, server = sock.recvfrom(4096)
                if checkEndingMessage(data):
                    continue
                else :
                    newFile.write(data.decode('utf8'))
                    print('file downloaded')
            else :
                errorMessage=data.decode('utf8').split()[2]
                print('Error: ' , code, errorMessage)
    
        if sendFile:
            f = open(filename,'r+')
            outputdata = f.read()
            message='POST'
            sent = sock.sendto(message.encode('utf8'), server_address)
            print ('sending "%s"' % f.name)
            sent = sock.sendto(f.name.encode('utf8'),server_address)
            sent = sock.sendto(outputdata.encode('utf8'), server_address)
            data, server = sock.recvfrom(4096)
            checkEndingMessage(data)

                
        print('\n\n')
    
    except Exception as info:
        print(info)
        
