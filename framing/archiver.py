#!/usr/bin/python3

import os


class Archiver:
    def __init__(self, files, folder):
        self.files = files
        self.folder = folder

    def writeByteArray(self, file, byteArray):
        singleFileInfo = {}
        file = open(file, 'rb')
        fileName = (file.name).encode()
        singleFileInfo["nameLength"] = f"{len(fileName):64d}".encode()
        singleFileInfo["name"] = fileName
        with file as f:
            lines = f.readlines()
            content = []
            contentLength = 0
            for line in lines:
                content.append(bytearray(line))
                contentLength += len(line)
            singleFileInfo["contentLength"] = f"{contentLength:64d}".encode()
            singleFileInfo["content"] = content
        byteArray.append(singleFileInfo)
        # os.remove(fileName)


    def readByteArray(self):
        archFile = open("arch.arch", 'rb')
        byteArray = []
        with archFile as f:
            archFileContents = f.read()

            while len(archFileContents) > 0:
                lengthName = int(archFileContents[0:64])
                archFileContents = archFileContents[64:]

                fileName = archFileContents[0:lengthName]
                archFileContents = archFileContents[lengthName:]

                contentLength = int(archFileContents[0:64])
                archFileContents = archFileContents[64:]

                content = (archFileContents[0:contentLength])
                archFileContents = archFileContents[contentLength:]

                byteArray.append([lengthName, fileName, contentLength, content])
        
        return byteArray

    def archive(self):
        archFile = open("arch.arch", "wb")
        byteArray = []
        for file in self.files:
            file = self.folder + file
            self.writeByteArray(file, byteArray)

        for file in byteArray:
            fileNameLength = file["nameLength"]
            fileName = file["name"]
            contentListLength = file["contentLength"]
            contentList = file["content"]
            archFile = open("arch.arch", "ab")
            archFile.write(fileNameLength)
            archFile.write(fileName)
            archFile.write(contentListLength)
            for content in contentList:
                archFile.write(content)
            archFile.close()

    def unarchive(self, name, contents):
        name = name.decode().split('/')
        name = name[1]
        try:
            os.remove("newFiles/" + name)
        except:
            pass
        newFile = open("newFiles/" + name, 'wb')
        newFile.write(contents)
        newFile.close()