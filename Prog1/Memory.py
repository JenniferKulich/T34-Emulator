import re
from intelhex import IntelHex
from Instructions import Instructions

class Memory:
    memoryList = [0] * 65536
    PC = 'start'
    PCForLookup = 1;



    OPRND = '-- --'
    AC = 0
    XR = 0
    YR = 0
    SP = 0xFF
    N = 0
    V = 0
    Dash = '1'
    B = 0
    D = 0
    I = 0
    Z = 0
    C = 0



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
        pad = start % 8
        padString = "   " * pad

        for i in range(start, end + 1):
            if i % 8 == 0 or start == i:
                print("\n" + "{0:0{1}X}".format(i, 2), end = "     ")
            if i == start:
                print(padString, end="")
            print("{0:0{1}X}".format(self.memoryList[i], 2), end = " ")
        print("\n")



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
        position = int(userInput, 16)
        count = 0
        self.N = 0
        self.V = 0
        self.B = 0
        self.D = 0
        self.I = 0
        self.Z = 0
        self.C = 0
        self.PCForLookup = '1'



        while(self.PCForLookup != '00'):
            self.PC = self.memoryList[position]
            self.PCForLookup = "{0:0{1}X}".format(self.PC, 2)

            self.INS = Instructions.instructions[str(self.PCForLookup)]['instruction']
            self.AMOD = Instructions.instructions[str(self.PCForLookup)]['AMOD']

            if(self.INS == 'ASL'):
                self.C = ( self.AC & 128 ) >> 7
                self.AC <<= 1
                self.AC &= 255
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'BRK'):
                #push PC+2, push SR
                self.I = 1
                self.B = 1
                #put all of the single things together and the put
                #in the memoryList at the stack pointer
                #put the first 8 bits and then the second 8 bits onto SP
                temp = self.N << 7
                temp = self.V << 6
                temp = self.B << 5
                temp = self.D << 4
                temp = self.I << 3
                temp = self.Z << 2
                temp = self.C << 1

                self.memoryList[self.SP] = temp
                self.SP = self.SP - 1


            elif(self.INS == 'CLC'):
                self.C = 0

            elif(self.INS == 'CLD'):
                self.D = 0

            elif(self.INS == 'CLI'):
                self.I = 0

            elif(self.INS == 'CLV'):
                self.V = 0

            elif self.INS == 'DEX':
                self.XR = self.XR - 1
                self.checkingNegativeAndZero(self.XR)
                self.XR &= 255

            elif self.INS == 'DEY':
                self.YR = self.YR - 1
                self.checkingNegativeAndZero(self.YR)
                self.YR &= 255

            elif(self.INS == 'INX'):
                self.XR = self.XR + 1
                self.checkingNegativeAndZero(self.XR)
                self.XR &= 255

            elif(self.INS == 'INY'):
                self.YR = self.YR + 1
                self.checkingNegativeAndZero(self.YR)
                self.YR &= 255

            elif(self.INS == 'LSR'):
                #shift one bit right (memory accumulator)
                self.C = self.AC & 1
                self.AC >>= 1
                if self.AC == 0:
                    self.Z  = 1
                else:
                    self.Z = 0

            elif(self.INS == 'NOP'):
                pass

            elif(self.INS == 'PHA'):
                #push the accumulator on the stack
                self.memoryList[self.SP] = self.AC
                self.SP -= 1

            elif(self.INS == 'PHP'):
                temp = self.N << 7
                temp = self.V << 6
                temp = self.B << 5
                temp = self.D << 4
                temp = self.I << 3
                temp = self.Z << 2
                temp = self.C << 1

                self.memoryList[self.SP] = temp
                self.SP = self.SP - 1

                #combine registers into one and then put where the
                #stack pointer is at and then decrement the SP
                #psh processor status on stack

            elif(self.INS == 'PLA'):
                #pull accumulator from stack
                self.SP += 1
                self.AC = self.memoryList[self.SP]
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'PLP'):
                self.SP += 1
                temp = self.memoryList[self.SP]
                self.N = temp >> 7
                self.V = temp >> 6
                self.B = temp >> 5
                self.D = temp >> 4
                self.I = temp >> 3
                self.Z = temp >> 2
                self.C = temp >> 1
                #opposite of PHP
                #pull processor status from stack


            elif(self.INS == 'ROL'):
                #rotate one bit left
                temp = self.C
                self.C = ( self.AC & 128 ) >> 7
                self.AC <<= 1
                self.AC |= temp
                self.AC &= 255
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'ROR'):
                #rotate one bit right
                temp = self.C
                self.C = self.AC & 1
                self.AC >>= 1
                self.AC |= temp << 7
                self.AC &= 255
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'SEC'):
                self.C = 1

            elif(self.INS == 'SED'):
                self.D = 1

            elif(self.INS == 'SEI'):
                self.I = 1

            elif(self.INS == 'TAX'):
                self.XR = self.AC
                self.checkingNegativeAndZero(self.XR)

            elif(self.INS == 'TAY'):
                self.YR = self.AC
                self.checkingNegativeAndZero(self.YR)

            elif(self.INS == 'TSX'):
                self.XR = self.SP
                self.checkingNegativeAndZero(self.XR)

            elif(self.INS == 'TXA'):
                self.AC = self.XR
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'TXS'):
                self.SP = self.XR

            elif(self.INS == 'TYA'):
                self.AC = self.YR
                self.checkingNegativeAndZero(self.AC)



            stringForA = "      "
            stringForAnythingElse = "   "


            stringToPrint = " " + hex(position) + "  " + "{0:0{1}X}".format(self.PC, 2) + "  " + str(self.INS)
            if self.AMOD == 'A':
                stringToPrint += stringForA
            else:
                stringToPrint += stringForAnythingElse
            stringToPrint += str(self.AMOD) + " " + self.OPRND + "  " + "{:02X}".format(self.AC) \
             + " " + "{:02X}".format(self.XR) + " " + "{:02X}".format(self.YR) + " " \
             + "{:02X}".format(self.SP) + " " + str(self.N) + str(self.V) + self.Dash + str(self.B) \
              + str(self.D) + str(self.I) + str(self.Z) + str(self.C)

            print(stringToPrint)
            stringToPrint = ""
            position = position + 1
            count = count + 1



    def FormatString(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")


    def checkingNegativeAndZero(self, register):
        if (register & 128) >> 7 == 1:
            self.N = 1
        else:
            self.N = 0
        if register == 00:
            self.Z == 1
        else:
            self.Z = 0
