#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
from archiver import Archiver
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

unarchiver = Archiver([], '')

while 1:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    if os.fork() == 0:
        numberOfFiles = int(conn.recv(64).decode())
        for i in range(numberOfFiles):
            print(i)
            lengthOfName = int(conn.recv(64).decode())
            fileName = conn.recv(lengthOfName)
            while lengthOfName < len(fileName):
                fileName += conn.recv(lengthOfName)

            lengthOfContent = int(conn.recv(64).decode())
            content = conn.recv(lengthOfContent)
            while lengthOfContent > len(content):
                content += conn.recv(lengthOfContent - len(content))
            
            unarchiver.unarchive(fileName, content)
        print("Zero length read")


# import threading
# prevent same files only