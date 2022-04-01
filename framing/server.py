#! /usr/bin/env python3

# Echo server program

from archiver import Archiver
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

# newArchiver = Archiver(['test.txt', 'test.java'], 'files/')
# newArchiver = Archiver(['test.txt'], 'files/')
newArchiver = Archiver(['img.png', 'test.java', 'test.txt'], 'files/')
# newArchiver = Archiver(['img.png','test.txt'], 'files/')
# newArchiver = Archiver(['img.png'], 'files/')


# number of files
# per file 
    # length of name
    # name
    # length of content
    # content

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        print('Connected by', addr)
        newArchiver.archive()
        byteArray = newArchiver.readByteArray()
        conn.send(f"{len(byteArray):64d}".encode())
        for file in byteArray:
            byteString = "".encode()
            lengthOfName = file[0]
            conn.send(f"{lengthOfName:64d}".encode())
            fileName = file[1]
            conn.send(fileName)
            lengthOfContent = file[2]
            conn.send(f"{lengthOfContent:64d}".encode())
            content = file[3]
            conn.send(content)
            # for content in file:
            #     if isinstance(content, int):
            #         # Length of file name or file contents
            #         byteString +=  f"{content:64d}".encode()
            #     else:
            #         # Actual file name or contents
            #         byteString += content
        #     conn.send(byteString)
        conn.shutdown(socket.SHUT_WR)


