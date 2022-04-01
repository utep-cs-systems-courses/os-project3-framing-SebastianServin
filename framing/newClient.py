#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import time
from archiver import Archiver
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

# newArchiver = Archiver(['test.txt', 'test.java'], 'files/')
# newArchiver = Archiver(['test.txt'], 'files/')
newArchiver = Archiver(['img.png', 'test.java', 'test.txt'], 'files/')
# newArchiver = Archiver(['img.png','test.txt'], 'files/')
# newArchiver = Archiver(['img.png'], 'files/')

newArchiver.archive()
byteArray = newArchiver.readByteArray()
time.sleep(5)
s.send(f"{len(byteArray):64d}".encode())
for file in byteArray:
    byteString = "".encode()
    lengthOfName = file[0]
    s.send(f"{lengthOfName:64d}".encode())
    fileName = file[1]
    s.send(fileName)
    lengthOfContent = file[2]
    s.send(f"{lengthOfContent:64d}".encode())
    content = file[3]
    s.send(content)

# s.shutdown(socket.SHUT_WR)      # no more output

