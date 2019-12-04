import re
from intelhex import IntelHex
from Instructions import Instructions

class Memory:
    memoryList = [0] * 65536
    PC = 'start'
    PCForLookup = 1;



    OPRND1 = 0
    OPRND2 = "--"
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
        if(re.match(r"([0-9a-fA-F]+)\.([0-9a-fA-F]+)", userInput)):
            return True
        else:
            return False

    def CheckIfStoringMemory(self, userInput):
        if(re.match(r"([0-9]*\:)([0-9]*)", userInput)):
            return True
        else:
            return False

    def CheckIfRunningProgram(self, userInput):
        return not self.CheckIfReturningMultipleMemory(userInput) and re.match(r"[0-9a-fA-F]+[R]", userInput)

    def PrintMultipleMemory(self, userInput):
        startAndEnd = self.GetStartAndEndMultipleMemoryLocation(userInput)
        start = int(startAndEnd[0], 16)
        end = int(startAndEnd[1], 16) + 1
        pad = start % 8
        padString = "   " * pad

        for i in range(start, end):
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
        self.OPRND1 = 0
        self.OPRND2 = "--"

        self.PCForLookup = '1'



        while(self.PCForLookup != '00'):
            self.PC = self.memoryList[position]
            self.PCForLookup = "{0:0{1}X}".format(self.PC, 2)

            self.INS = Instructions.instructions[str(self.PCForLookup)]['instruction']
            self.AMOD = Instructions.instructions[str(self.PCForLookup)]['AMOD']

            if(self.INS == 'ASL' and self.PCForLookup == '0A'):
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
                self.SP = self.SP - 3
                self.OPRND1 = "--"


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

            elif(self.INS == 'LSR' and self.PCForLookup == '4A'):
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


            elif(self.INS == 'ROL' and self.PCForLookup == '2A'):
                #rotate one bit left
                temp = self.C
                self.C = ( self.AC & 128 ) >> 7
                self.AC <<= 1
                self.AC |= temp
                self.AC &= 255
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'ROR' and self.PCForLookup == '6A'):
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


#for the C grade functions
            elif(self.INS =='ADC' and self.PCForLookup == '69'):
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC + temp
                if(self.C == 1):
                    self.AC = self.AC + 1
                self.AC = self.AC & 255
                self.OPRND1 = int(self.memoryList[position])
                position = position - 1

            elif(self.INS == 'ADC' and self.PCForLookup == '65'):
#not tested but should be the same
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC + self.memoryList[temp]
                if(self.C == 1):
                    self.AC = self.AC + 1
                self.AC = self.AC & 255
        #think this is correct- probably not
                self.OPRND1 = self.memoryList[position]
                position = position - 1

            elif(self.INS == 'AND' and self.PCForLookup == '29'):
#not tested, but should be correct because of the next one that was tested
                position = position + 1
                self.AC = self.AC & self.memoryList[position]
                self.OPRND1 = self.memoryList[position]
                self.checkingNegativeAndZero[self.AC]
                position = position - 1
            
            elif(self.INS == 'AND' and self.PCForLookup == '25'):
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC  & self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.AC)
                position = position - 1

            elif(self.INS == 'ASL' and self.PCForLookup == '06'):
#not tested but may be correct because of the one from last program
#probably not because I'm such a dumbass
                position = position + 1
                temp = self.memoryList[position]
                self.C = ( self.memoryList[temp] & 128 ) >> 7
                self.memoryList[temp] <<= 1
                self.memoryList[temp] &= 255
                self.checkingNegativeAndZero(self.memoryList[temp])
                position = position - 1


            elif(self.INS == 'CMP' and self.PCForLookup == 'C9'):
                position = position + 1
                twosComp = ~self.memoryList[position] + 1
                temp = self.AC + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[position]
                position = position -1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CMP' and self.PCForLookup == 'C5'):
#not tested
                position = position + 1
                temp = self.memoryList[position]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.AC + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                position = position - 1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPX' and self.PCForLookup == 'E0'):
#not tested
                position = position + 1
                twosComp = ~self.memoryList[position] + 1
                temp = self.XR + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[position]
                position = position -1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPX' and self.PCForLookup == 'E4'):
#not tested
                position = position + 1
                temp = self.memoryList[position]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.XR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                position = position - 1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPY' and self.PCForLookup == 'C0'):
#not tested
                position = position + 1
                twosComp = ~self.memoryList[position] + 1
                temp = self.YR + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[position]
                position = position -1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPY' and self.PCForLookup == 'C4'):
#not tested
                position = position + 1
                temp = self.memoryList[position]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.YR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                position = position - 1
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'DEC' and self.PCForLookup == 'C6'):
#not tested
                position = position - 1
                temp = self.memoryList[position]
                self.memoryList[temp] = self.memoryList[temp] - 1
                self.checkingNegativeAndZero(self.memoryList[temp])
                position = position + 1

            elif(self.INS == 'EOR' and self.PCForLookup == '49'):
                position = position + 1
                self.AC = self.AC ^ self.memoryList[position]
                self.OPRND1 = self.memoryList[position]
                self.checkingNegativeAndZero(self.AC)
                position = position - 1

            elif(self.INS == 'EOR' and self.PCForLookup == '45'):
#have not tested yet
                position = position + 1
                temp = self.memoryList[position]
                numToEOR = self.memoryList[temp]
                self.AC = self.AC ^ numToEOR           
                self.checkingNegativeAndZero(self.AC)
                position = position - 1

            elif(self.INS == 'INC' and self.PCForLookup == 'E6'):
                #memory + 1 -> memory in the next location
                position = position + 1
                temp = self.memoryList[position]
                numToInc = self.memoryList[temp]
                numToInc = numToInc + 1
                self.memoryList[temp] = numToInc
#not sure what to check here
                #self.checkingNegativeAndZero(self.XR)
                position = position - 1


            elif(self.INS == 'LDA' and self.PCForLookup == 'A9'):
                position = position + 1
                self.AC = self.memoryList[position]
                self.OPRND1 = self.AC
                self.checkingNegativeAndZero(self.AC)
                position = position - 1

            elif(self.INS == 'LDA' and self.PCForLookup == 'A5'):
                position = position + 1
                #get the memo[pos] and then go to that part of the memory and get what's there and put into AC
                temp = self.memoryList[position]
                self.OPRND1 = self.memoryList[position]
                self.AC = self.memoryList[temp]
                self.checkingNegativeAndZero(self.AC)
                position = position - 1

            elif(self.INS == 'LDX' and self.PCForLookup == 'A2'):
                position = position + 1
                self.OPRND1 = int(self.memoryList[position])
                self.XR = self.XR + self.memoryList[position]
                self.checkingNegativeAndZero(self.XR)
                position = position - 1
            
            elif(self.INS == 'LDX' and self.PCForLookup == 'A6'):
                position = position + 1
                temp = self.memoryList[position]
                self.XR = self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.XR)
                position = position - 1 

            elif(self.INS == 'LDY' and self.PCForLookup == 'A0'):
#not tested- but LDX was tested, so should be correct
                position = position + 1
                self.OPRND1 = self.memoryList[position]
                self.YR = self.YR + self.memoryList[position]
                self.checkingNegativeAndZero(self.YR)
                position = position - 1

            elif(self.INS == 'LDY' and self.PCForLookup == 'A4'):
#not tested- but LDX was tested, so should be correct
                position = position + 1
                temp = self.memoryList[position]
                self.YR = self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.YR)
                position = position - 1 

            elif(self.INS == 'LSR' and self.PCForLookup == '46'):
#I'm haven't done the fucking shifts on this one
                position = position + 1
                temp = self.memoryList[position]
                self.OPRND1 = temp
                position = position - 1

            elif(self.INS == 'ORA' and self.PCForLookup == '09'):
#not testd, but taken from AND one which was based off of the tested AND one, so should be correct unless
#I'm being a dumb bitch like usual
                position = position + 1
                self.AC = self.AC | self.memoryList[position]
                self.OPRND1 = self.memoryList[position]
                self.checkingNegativeAndZero[self.AC]
                position = position - 1


            elif(self.INS == 'ORA' and self.PCForLookup == '05'):
#not tested, but taken from AND one, so should be right
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC  | self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.AC)
                position = position - 1


            elif(self.INS == 'ROL' and self.PCForLookup == '26'):
#not tested but probably close because of the last one- using the memory insead of AC
#ask Nate how you did it because you're too dumb to actually have gotten it correct
                position = position + 1
                fromMemory = self.memoryList[position]
                temp = self.C
                self.C = (spotInMem & 128 ) >> 7
                self.memoryList[fromMemory] <<= 1
                self.memoryList[fromMemory] |= temp
                self.memoryList[fromMemory] &= 255
                self.checkingNegativeAndZero(self.memoryList[fromMemory])
                position = position - 1

            elif(self.INS == 'ROR' and self.PCForLookup == '66'):
#took from last one but probably way off because I'm a dumbass, so ask Nate what he did
                position = position + 1
                fromMemory = self.memoryList[position]
                temp = self.C
                self.C = self.AC & 1
                self.memoryList[fromMemory] >>= 1
                self.memoryList[fromMemory] |= temp << 7
                self.memoryList[fromMemory] &= 255
                self.checkingNegativeAndZero(self.memoryList[fromMemory])
                position = position - 1

            elif(self.INS == 'SBC' and self.PCForLookup == 'E9'):
#not tested, but should be sort of correct because of tested one
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC - temp
                if(self.C == 1):
                    self.AC = self.AC - 1
                self.AC = self.AC & 255
                self.OPRND1 = self.memoryList[position]
                position = position - 1


            elif(self.INS == 'SBC' and self.PCForLookup == 'E5'):
#not tested and probably really wrong because I'm a dumbass
                position = position + 1
                temp = self.memoryList[position]
                self.AC = self.AC - self.memoryList[temp]
                if(self.C == 1):
                    self.AC = self.AC - 1
                self.AC = self.AC & 255
        #think this is correct- probably not
                self.OPRND1 = self.memoryList[position]
                position = position - 1


            elif(self.INS == 'STA' and self.PCForLookup == '85'):
                #get mem[position] and then sta with whatever and mem[pos]
                position = position + 1
                temp = self.memoryList[position]
                self.memoryList[temp] = self.AC
                position = position - 1

            elif(self.INS == 'STX' and self.PCForLookup == '86'):
                position = position + 1
                temp = self.memoryList[position]
                self.memoryList[temp] = self.XR
                self.OPRND1 = temp
                position = position - 1

            elif(self.INS == 'STY' and self.PCForLookup == '84'):
#not tested
                position = position + 1
                temp = self.memoryList[position]
                self.memoryList[temp] = self.YR
                position = position - 1


#for the B grades 
            elif(self.INS == 'ADC' and self.PCForLookup == '6D'):
                pass
            elif(self.INS == 'AND' and self.PCForLookup == '2D'):
                pass
            elif(self.INS == 'ASL' and self.PCForLookup == '0E'):
                pass
            elif(self.INS == 'BCC' and self.PCForLookup == '90'):
                pass
            elif(self.INS == 'BSC' and self.PCForLookup == '84'):
                pass
            elif(self.INS == 'BEQ' and self.PCForLookup == 'F0'):
                pass
            elif(self.INS == 'BIT' and self.PCForLookup == '2C'):
                pass
            elif(self.INS == 'BMI' and self.PCForLookup == '30'):
                pass
            elif(self.INS == 'BNE' and self.PCForLookup == 'D0'):
                pass
            elif(self.INS == 'BPL' and self.PCForLookup == '10'):
                pass
            elif(self.INS == 'BVC' and self.PCForLookup == '50'):
                pass
            elif(self.INS == 'BVS' and self.PCForLookup == '70'):
                pass
            elif(self.INS == 'CMP' and self.PCForLookup == 'CD'):
                pass
            elif(self.INS == 'CPX' and self.PCForLookup == 'EC'):
                pass
            elif(self.INS == 'CPY' and self.PCForLookup == 'CC'):
                pass
            elif(self.INS == 'DEC' and self.PCForLookup == 'CE'):
                pass
            elif(self.INS == 'EOR' and self.PCForLookup == '4D'):
                pass
            elif(self.INS == 'INC' and self.PCForLookup == 'EE'):
                pass
            elif(self.INS == 'JMP' and self.PCForLookup == '4C'):
                pass
            elif(self.INS == 'JSR' and self.PCForLookup == '20'):
                pass
            elif(self.INS == 'LDA' and self.PCForLookup == 'AD'):
                pass
            elif(self.INS == 'LDX' and self.PCForLookup == 'AE'):
                pass
            elif(self.INS == 'LDY' and self.PCForLookup == 'AC'):
                pass
            elif(self.INS == 'LSR' and self.PCForLookup == '4E'):
                pass
            elif(self.INS == 'ORA' and self.PCForLookup == '0D'):
                pass
            elif(self.INS == 'ROL' and self.PCForLookup == '2E'):
                pass
            elif(self.INS == 'ROR' and self.PCForLookup == '6E'):
                pass
            elif(self.INS == 'RTS' and self.PCForLookup == '60'):
                pass
            elif(self.INS == 'SBC' and self.PCForLookup == 'ED'):
                pass
            elif(self.INS == 'STA' and self.PCForLookup == '8D'):
                pass
            elif(self.INS == 'STX' and self.PCForLookup == '8E'):
                pass
            elif(self.INS == 'STY' and self.PCForLookup == '8C'):
                pass

#printing
            stringForA = "      "
            stringForZpg = "    "
            stringForAnythingElse = "   "

            stringToPrint = " " + hex(position)[2:] + "  " + "{0:0{1}X}".format(self.PC, 2) + "  " + str(self.INS)

            if self.AMOD == 'A' or self.AMOD == '#':
                stringToPrint += stringForA
            elif self.AMOD == 'zpg' or self.AMOD == 'abs' or self.AMOD == 'rel':
                stringToPrint += stringForZpg
            else:
                stringToPrint += stringForAnythingElse

            stringToPrint += str(self.AMOD) + " " 

            if(self.INS == 'BRK'):
                stringToPrint += self.OPRND1
            else:
                stringToPrint += "{:02X}".format(self.OPRND1)

            stringToPrint += " " + str(self.OPRND2) + "  " + "{:02X}".format(self.AC) \
             + " " + "{:02X}".format(self.XR) + " " + "{:02X}".format(self.YR) + " " \
             + "{:02X}".format(self.SP) + " " + str(self.N) + str(self.V) + self.Dash + str(self.B) \
              + str(self.D) + str(self.I) + str(self.Z) + str(self.C)

            print(stringToPrint)
            stringToPrint = ""
            position = position + 1
            count = count + 1
            if(self.AMOD == '#' or self.AMOD == 'zpg'):
                position = position + 1



    def FormatString(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")


    def checkingNegativeAndZero(self, register):
        if register == 0:
            self.Z = 1
        else:
            self.Z = 0

        if (register & 128) >> 7 == 1:
            self.N = 1
        else:
            self.N = 0
