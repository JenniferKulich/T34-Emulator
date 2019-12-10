import re
from intelhex import IntelHex
from Instructions import Instructions

class Memory:
    memoryList = [0] * 65536
    PC = 'start'
    OPCode = 1;



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
        self.PC = int(userInput, 16)
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

        self.OPCode = '1'
        self.PCStrorage = 0
        self.newPC = 0
        self.offset = 0



        while(self.OPCode != '00'):
            self.OPCode = "{0:0{1}X}".format(self.memoryList[self.PC], 2)
            self.INS = Instructions.instructions[str(self.OPCode)]['instruction']
            self.AMOD = Instructions.instructions[str(self.OPCode)]['AMOD']

            if(self.INS == 'ASL' and self.OPCode == '0A'):
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
                self.OPRND1 = "--"
                self.OPRND2 = "--"

            elif(self.INS == 'CLD'):
                self.D = 0
                self.OPRND1 = "--"
                self.OPRND2 = "--"

            elif(self.INS == 'CLI'):
                self.I = 0
                self.OPRND1 = "--"
                self.OPRND2 = "--"

            elif(self.INS == 'CLV'):
                self.V = 0
                self.OPRND1 = "--"
                self.OPRND2 = "--"

            elif self.INS == 'DEX':
                self.XR = self.XR - 1
                self.checkingNegativeAndZero(self.XR)
                self.XR &= 255

            elif self.INS == 'DEY':
                self.YR = self.YR - 1
                self.YR &= 255
                self.checkingNegativeAndZero(self.YR)
                self.OPRND1 = "--"
                self.OPRND2 = '--'

            elif(self.INS == 'INX'):
                self.XR = self.XR + 1
                self.checkingNegativeAndZero(self.XR)
                self.XR &= 255

            elif(self.INS == 'INY'):
                self.YR = self.YR + 1
                self.checkingNegativeAndZero(self.YR)
                self.YR &= 255

            elif(self.INS == 'LSR' and self.OPCode == '4A'):
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


            elif(self.INS == 'ROL' and self.OPCode == '2A'):
                #rotate one bit left
                temp = self.C
                self.C = ( self.AC & 128 ) >> 7
                self.AC <<= 1
                self.AC |= temp
                self.AC &= 255
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'ROR' and self.OPCode == '6A'):
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
            elif(self.INS =='ADC' and self.OPCode == '69'):
                temp = self.memoryList[self.PC + 1]
                self.AC = self.AC + temp
                if(self.C == 1):
                    self.AC = self.AC + 1
                self.OPRND1 = int(self.memoryList[self.PC + 1])
                self.checkForCarrySet(self.AC)
                self.AC = self.AC & 255

            elif(self.INS == 'ADC' and self.OPCode == '65'):
                temp = self.memoryList[self.PC + 1] 
                self.AC = self.AC + self.memoryList[temp]
                if(self.C == 1):
                    self.AC = self.AC + 1
                self.OPRND1 = self.memoryList[temp]
                self.checkForCarrySet(self.AC)
                self.AC = self.AC & 255

            elif(self.INS == 'AND' and self.OPCode == '29'):
                self.AC = self.AC & self.memoryList[self.PC + 1]
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero[self.AC]
            
            elif(self.INS == 'AND' and self.OPCode == '25'):
                temp = self.memoryList[self.PC + 1]
                self.AC = self.AC  & self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'ASL' and self.OPCode == '06'):
                temp = self.memoryList[self.PC + 1]
                self.C = ( self.memoryList[temp] & 128 ) >> 7
                self.memoryList[temp] <<= 1
                self.memoryList[temp] &= 255
                self.checkingNegativeAndZero(self.memoryList[temp])
                self.checkForCarrySet(self.memoryList[temp])

            elif(self.INS == 'CMP' and self.OPCode == 'C9'):
                twosComp = ~self.memoryList[self.PC + 1] + 1
                temp = self.AC + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[self.PC + 1]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CMP' and self.OPCode == 'C5'):
                temp = self.memoryList[self.PC + 1]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.AC + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPX' and self.OPCode == 'E0'):
                twosComp = ~self.memoryList[self.PC + 1] + 1
                temp = self.XR + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[self.PC + 1]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPX' and self.OPCode == 'E4'):
                temp = self.memoryList[self.PC + 1]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.XR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPY' and self.OPCode == 'C0'):
                twosComp = ~self.memoryList[self.PC + 1] + 1
                temp = self.YR + twosComp
                checkForCarry = temp & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 = self.memoryList[self.PC + 1]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPY' and self.OPCode == 'C4'):
                temp = self.memoryList[self.PC + 1]
                twosComp = ~self.memoryList[temp] + 1
                operation = self.YR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'DEC' and self.OPCode == 'C6'):
                temp = self.memoryList[self.PC + 1]
                self.memoryList[temp] = self.memoryList[temp] - 1
                self.checkingNegativeAndZero(self.memoryList[temp])

            elif(self.INS == 'EOR' and self.OPCode == '49'):
                self.AC = self.AC ^ self.memoryList[self.PC + 1]
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'EOR' and self.OPCode == '45'):
                temp = self.memoryList[self.PC + 1]
                numToEOR = self.memoryList[temp]
                self.AC = self.AC ^ numToEOR           
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'INC' and self.OPCode == 'E6'):
                #memory + 1 -> memory in the next location
                temp = self.memoryList[self.PC + 1]
                self.memoryList[temp] = self.memoryList[temp] + 1
                self.checkingNegativeAndZero(self.memoryList[temp])


            elif(self.INS == 'LDA' and self.OPCode == 'A9'):
                self.AC = self.memoryList[self.PC + 1]
                self.OPRND1 = self.AC
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'LDA' and self.OPCode == 'A5'):
                #get the memo[pos] and then go to that part of the memory and get what's there and put into AC
                temp = self.memoryList[self.PC + 1]
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.AC = self.memoryList[temp]
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'LDX' and self.OPCode == 'A2'):
                self.OPRND1 = int(self.memoryList[self.PC + 1])
                self.XR = self.XR + self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero(self.XR)
            
            elif(self.INS == 'LDX' and self.OPCode == 'A6'):
                temp = self.memoryList[self.PC + 1]
                self.XR = self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.XR)

            elif(self.INS == 'LDY' and self.OPCode == 'A0'):
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.YR = self.YR + self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero(self.YR)

            elif(self.INS == 'LDY' and self.OPCode == 'A4'):
                temp = self.memoryList[self.PC + 1]
                self.YR = self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.YR)

            elif(self.INS == 'LSR' and self.OPCode == '46'):
                fromMemory = self.memoryList[self.PC + 1]
                self.C = self.memoryList[fromMemory] & 1
                self.memoryList[fromMemory] >>= 1
                if sself.memoryList[fromMemory] == 0:
                    self.Z  = 1
                else:
                    self.Z = 0
                self.OPRND1 = self.memoryList[fromMemory]

            elif(self.INS == 'ORA' and self.OPCode == '09'):
                self.AC = self.AC | self.memoryList[self.PC + 1]
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero[self.AC]


            elif(self.INS == 'ORA' and self.OPCode == '05'):
                temp = self.memoryList[self.PC + 1]
                self.AC = self.AC  | self.memoryList[temp]
                self.OPRND1 = temp
                self.checkingNegativeAndZero(self.AC)


            elif(self.INS == 'ROL' and self.OPCode == '26'):
                fromMemory = self.memoryList[self.PC + 1]
                temp = self.C
                self.C = (self.memoryList[fromMemory] & 128 ) >> 7
                self.memoryList[fromMemory] <<= 1
                self.memoryList[fromMemory] |= temp
                self.memoryList[fromMemory] &= 255
                self.checkingNegativeAndZero(self.memoryList[fromMemory])

            elif(self.INS == 'ROR' and self.OPCode == '66'):
                fromMemory = self.memoryList[self.PC + 1]
                temp = self.C
                self.C = self.memoryList[fromMemory] & 1
                self.memoryList[fromMemory] >>= 1
                self.memoryList[fromMemory] |= temp << 7
                self.memoryList[fromMemory] &= 255
                self.checkingNegativeAndZero(self.memoryList[fromMemory])

            elif(self.INS == 'SBC' and self.OPCode == 'E9'):
                temp = self.memoryList[self.PC + 1]
                self.AC = self.AC - temp
                if(self.C == 0):
                    self.AC = self.AC - 1
                self.AC = self.AC & 255
                self.OPRND1 = self.memoryList[self.PC + 1]
                self.checkingNegativeAndZero(self.AC)


            elif(self.INS == 'SBC' and self.OPCode == 'E5'):
                temp = self.memoryList[self.PC + 1]
                self.AC = self.AC - self.memoryList[temp]
                if(self.C == 0):
                    self.AC = self.AC - 1
                self.AC = self.AC & 255
                self.OPRND1 = self.memoryList[temp]
                self.checkingNegativeAndZero(self.AC)


            elif(self.INS == 'STA' and self.OPCode == '85'):
                #get mem[position] and then sta with whatever and mem[pos]
                temp = self.memoryList[self.PC + 1]
                self.OPRND1 = temp
                self.memoryList[temp] = self.AC


            elif(self.INS == 'STX' and self.OPCode == '86'):
                temp = self.memoryList[self.PC + 1]
                self.memoryList[temp] = self.XR
                self.OPRND1 = temp

            elif(self.INS == 'STY' and self.OPCode == '84'):
                temp = self.memoryList[self.PC + 1]
                self.memoryList[temp] = self.YR
                self.OPRND1 = temp


#for the B grades 
            elif(self.INS == 'ADC' and self.OPCode == '6D'):
                temp = self.getOPRNDandTemp()
                self.AC = self.AC + self.memoryList[temp]
                if(self.C == 1):
                    self.AC = self.AC + 1
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'AND' and self.OPCode == '2D'):
#not tested but taken from code that was tested
                temp = self.getOPRNDandTemp()
                self.AC = self.AC & self.memoryList[temp]
                self.checkingNegativeAndZero[self.AC]

            elif(self.INS == 'ASL' and self.OPCode == '0E'):
#need to move into SR
                temp = self.getOPRNDandTemp()

            elif(self.INS == 'BCC' and self.OPCode == '90'):
                self.branching(self.C, 0)
                  

            elif(self.INS == 'BSC' and self.OPCode == 'BO'):
#not tested but based off of BCC- tested
                self.branching(self.C, 1)


            elif(self.INS == 'BEQ' and self.OPCode == 'F0'):
#not tested but based off of BCC- tested
                self.branching(self.Z, 1)


            elif(self.INS == 'BIT' and self.OPCode == '2C'):
#need to get the top 2 bits
                temp = self.getOPRNDandTemp()
                operation = self.AC & self.memoryList[temp]
                self.checkingNegativeAndZero(operation)

        



            elif(self.INS == 'BMI' and self.OPCode == '30'):
#not tested but based off of BCC- tested
                self.branching(self.N, 1)


            elif(self.INS == 'BNE' and self.OPCode == 'D0'):
                self.branching(self.Z, 0)


            elif(self.INS == 'BPL' and self.OPCode == '10'):
#not tested but based off of BCC- tested
                self.branching(self.N, 0)

            elif(self.INS == 'BVC' and self.OPCode == '50'):
#not tested but based off of BCC- tested
                self.branching(self.V, 0)

            elif(self.INS == 'BVS' and self.OPCode == '70'):
#not tested but based off of BCC- tested
                self.branching(self.V, 1)
                
            elif(self.INS == 'CMP' and self.OPCode == 'CD'):
                temp = self.getOPRNDandTemp()
                twosComp = ~self.memoryList[temp] + 1
                operation = self.AC + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPX' and self.OPCode == 'EC'):
                temp = self.getOPRNDandTemp()
                twosComp = ~self.memoryList[temp] + 1
                operation = self.XR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp == 0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0

            elif(self.INS == 'CPY' and self.OPCode == 'CC'):
                temp = self.getOPRNDandTemp()
                twosComp = ~self.memoryList[temp] + 1
                operation = self.YR + twosComp
                checkForCarry = operation & 256
                if(checkForCarry > 0 or twosComp ==0):
                    self.C = 1
                self.checkingNegativeAndZero(temp)
                self.OPRND1 - self.memoryList[temp]
                if(self.C == 1):
                    self.N = 0


            elif(self.INS == 'DEC' and self.OPCode == 'CE'):
#not tested but taken from one that was tested
                temp = self.getOPRNDandTemp()
                self.memoryList[temp] = self.memoryList[temp] - 1
                self.checkingNegativeAndZero(self.memoryList[temp])

            elif(self.INS == 'EOR' and self.OPCode == '4D'):
#not tested but taken from one that was tested
                temp = self.getOPRNDandTemp()
                self.AC = self.AC ^ self.memoryList[temp]
                self.checkingNegativeAndZero(self.AC)

            elif(self.INS == 'INC' and self.OPCode == 'EE'):
#not tested but taken from one that was tested
                temp = self.getOPRNDandTemp()
                self.memoryList[temp] = self.memoryList[temp] + 1
                self.checkingNegativeAndZero(self.memoryList[temp])


            elif(self.INS == 'JMP' and self.OPCode == '6C'):
#aw hell no. I have no idea what this is doing- wtf is up with the PC???
                temp = self.getOPRNDandTemp()
                operand1 = self.memoryList[temp]  
                operand2 = self.memoryList[temp + 1]
                self.newPC = operand2
                self.newPC <<= 8
                self.newPC = operand1 | self.newPC

            elif(self.INS == 'JSR' and self.OPCode == '20'):
#if I am told I have done ths wrong, I will actually cry
                temp = self.getOPRNDandTemp()
                lowO = self.PC & 0xFF
                highO = self.PC & 0xFF00
                highO >>= 8
                self.memoryList[self.SP] = highO
                self.memoryList[self.SP - 1] = lowO     
                self.SP = self.SP - 2
                self.newPC = temp

            elif(self.INS == 'LDA' and self.OPCode == 'AD'):
                temp = self.getOPRNDandTemp()
                self.AC = self.memoryList[temp]  
                self.checkingNegativeAndZero(self.AC)              

            elif(self.INS == 'LDX' and self.OPCode == 'AE'):
                temp = self.getOPRNDandTemp()
                self.XR = self.XR + self.memoryList[temp]
                self.checkingNegativeAndZero(self.XR)

            elif(self.INS == 'LDY' and self.OPCode == 'AC'):
                temp = self.getOPRNDandTemp()
                self.YR = self.YR + self.memoryList[temp]
                self.checkingNegativeAndZero(self.YR)

            elif(self.INS == 'LSR' and self.OPCode == '4E'):
                pass
            elif(self.INS == 'ORA' and self.OPCode == '0D'):
                temp = self.getOPRNDandTemp()
                self.AC = self.AC | self.memoryList[temp]

            elif(self.INS == 'ROL' and self.OPCode == '2E'):
                pass

            elif(self.INS == 'ROR' and self.OPCode == '6E'):
#need to move into SR
                temp = self.getOPRNDandTemp()

            elif(self.INS == 'RTS' and self.OPCode == '60'):
                self.OPRND1 = "--"
                self.OPRND2 = "--"
                operand1 = self.memoryList[self.SP + 1]
                operand2 = self.memoryList[self.SP + 2]
                self.SP = self.SP + 2
                temp = operand2 
                temp <<= 8
                temp = operand1 | temp
                
                self.newPC = temp + 3

                



            elif(self.INS == 'SBC' and self.OPCode == 'ED'):
                pass
            elif(self.INS == 'STA' and self.OPCode == '8D'):
                temp = self.getOPRNDandTemp()
                self.memoryList[temp] = self.AC

            elif(self.INS == 'STX' and self.OPCode == '8E'):
#not tested but taken from one that's been tested
                temp = self.getOPRNDandTemp()
                self.memoryList[temp] = self.XR

            elif(self.INS == 'STY' and self.OPCode == '8C'):
#not tested but taken from one that's been tested
                temp = self.getOPRNDandTemp()
                self.memoryList[temp] = self.YR


#printing
            stringForA = "      "
            stringForZpg = "    "
            stringForAnythingElse = "   "

            stringToPrint = " " + hex(self.PC)[2:] + "  " + self.OPCode + "  " + str(self.INS)

            if self.AMOD == 'A' or self.AMOD == '#':
                stringToPrint += stringForA
            elif self.AMOD == 'zpg' or self.AMOD == 'abs' or self.AMOD == 'rel' or self.AMOD == 'ind':
                stringToPrint += stringForZpg
            else:
                stringToPrint += stringForAnythingElse

            stringToPrint += str(self.AMOD) + " " 

            if(self.INS == 'BRK'):
                stringToPrint +=  "-- --"
            elif(self.OPRND1 == "--" and self.OPRND2 == "--"):
                stringToPrint += self.OPRND1 + " " + self.OPRND2
            else:
                stringToPrint += "{:02X}".format(self.OPRND1) + " "
                if(self.OPRND2 == "--"):
                    stringToPrint += str(self.OPRND2)
                else:
                    stringToPrint += "{:02X}".format(self.OPRND2)

            stringToPrint += "  " + "{:02X}".format(self.AC) \
             + " " + "{:02X}".format(self.XR) + " " + "{:02X}".format(self.YR) + " " \
             + "{:02X}".format(self.SP) + " " + str(self.N) + str(self.V) + self.Dash + str(self.B) \
              + str(self.D) + str(self.I) + str(self.Z) + str(self.C)

            print(stringToPrint)
            stringToPrint = ""
#Jennifer- check against all branching operands- make function for it
            if(not self.checkIfBranchingCode() and self.INS != 'JMP' and self.INS != 'JSR' and self.INS != 'RTS'):
                self.PC = self.PC + 1
                count = count + 1
                if(self.AMOD == '#' or self.AMOD == 'zpg'):
                    self.PC = self.PC + 1
                if(self.AMOD == "abs"):
                    self.PC = self.PC + 2

            if(self.INS == 'JMP' and self.OPCode == '6C'):
                self.PC = self.newPC

            if(self.INS == 'JSR'):
                self.PC = self.newPC

            if(self.INS == 'RTS' ):
                self.PC = self.newPC

            if(self.checkIfBranchingCode()):
                self.PC = self.newPC
                



    def FormatString(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    def checkIfBranchingCode(self):
        if(self.INS == 'BCC' or self.INS == 'BCS' or self.INS == 'BEQ' or self.INS == 'BMI'
        or self.INS == 'BNE' or self.INS == 'BPL' or self.INS == 'BVC' or self.INS == 'BVS'):
            return True
        return False

    def checkingNegativeAndZero(self, register):
        if register == 0:
            self.Z = 1
        else:
            self.Z = 0

        if (register & 128) >> 7 == 1:
            self.N = 1
        else:
            self.N = 0
    
    def checkForCarrySet(self, register):
        temp = register & 256
        if(temp > 0):
            self.C = 1
        else:
            self.C = 0

    def getOPRNDandTemp(self):
        self.OPRND1 = self.memoryList[self.PC + 1]
        self.OPRND2 = self.memoryList[self.PC + 2]
        temp = self.OPRND2 
        temp <<= 8
        temp = self.OPRND1| temp
        return temp

    def reverseTwosComp(self, value):
        value = 255 - value
        value = value + 1
        value = -value
        return value

    def signExtendedSubtraction(self, value1, value2):
        value1 = sign_extend(value1, 8)
        value2 = sign_extend(value2, 8)
        return value1 - value2 

    def signExtendedAdditionForBranch(self, value1, value2):
        if(value1 > 127):
            value1 = self.reverseTwosComp(value1)
        temp = value1 + value2
        return temp  
   
    def branching(self, flag, flagSet):
        self.OPRND1 = self.memoryList[self.PC + 1]
        self.OPRND2 = "--"
        if(flag == flagSet):
            self.newPC = self.signExtendedAdditionForBranch(self.OPRND1, self.PC + 1) + 1 
        else: 
            self.newPC = self.PC + 2



