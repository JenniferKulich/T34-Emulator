import re
from intelhex import IntelHex

class Memory:
    memoryList = [0] * 65536
    programCounter = 0

    def LoadFromFile(self, fileName):
        intelHex = IntelHex(fileName)
        for addr, dat in intelHex.todict().items():
            self.memoryList[addr] = dat

    def CheckIfReturningMultipleMemory(self, userInput):
        if(re.match(r"([0-9]*)\.([0-9]*[a-zA-Z]*)", userInput)):
            return True
        else:
            return False

    def CheckIfStoringMemory(self, userInput):
        if(re.match(r"([0-9]*\:)([0-9]*)", userInput)):
            return True
        else:
            return False

    def CheckIfRunningProgram(self, userInput):
        if(self.CheckIfReturningMultipleMemory(userInput) == False
        and re.match(r"[0-9]*[R]", userInput)):
            return True
        else:
            return False

    def PrintMultipleMemory(self, userInput):
        startAndEnd = self.GetStartAndEndMultipleMemoryLocation(userInput)
        start = int(startAndEnd[0], 16)
        end = int(startAndEnd[1], 16) + 1
        count = 0
        pad = start % 8
        padString = "   " * pad

        for i in range(start, end):
            if(count == 0):
                print("{0:0{1}X}".format(count + i, 1), end = "  " + padString)
                count = count + pad
            if(count > 0 and count % 8 == 0):
                print()
                print("{0:0{1}X}".format(start + count, 1), end = "  ")
            print("{0:0{1}X}".format(self.memoryList[i], 2), end = ' ')
            if(i == end - 1):
                print()
            count = count + 1;


    def GetStartAndEndMultipleMemoryLocation(self, userInput):
        return userInput.split(".");

    #need to check that it won't step out of bounds of array
    def StoreInMemory(self, userInput):
        start, data = self.GetStartAndItemsForStoring(userInput)
        start = int(start, 16)
        end = len(data)

        for i in range(0, end):
            self.memoryList[start + i] = int(data[i], 16)

    def GetStartAndItemsForStoring(self, userInput):
        #split on the :
        splitOnColon = userInput.split(':')
        #take the second index and split them on the spaces
        splitOnSpaces = splitOnColon[1].split(' ')
        #check if the first one was a space
        if(splitOnSpaces[0] == ""):
            splitOnSpaces.pop(0)
        return splitOnColon[0], splitOnSpaces;

    def ReturningOneMemory(self, userInput):
        print(userInput, end = "  ")
        print("{0:0{1}X}".format(self.memoryList[int(userInput, 16)], 2))

    def PrintRunningProgram(self, userInput):
        self.FormatString();
        userInput = userInput[:-1]
        print(" " + userInput)
        programCounter = userInput

    def FormatString(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")
