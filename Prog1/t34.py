import sys
from Memory import Memory

memory = Memory()

if (len(sys.argv) >= 2):
    memory.LoadFromFile(sys.argv[1])

userInput = ""

while userInput != "exit":
    try:
        userInput = input("> ")
    except Exception as e:
        sys.exit(e)
    except KeyboardInterrupt as i:
        sys.exit(i)

    if(userInput != "exit"):
        if(memory.CheckIfReturningMultipleMemory(userInput)):
            memory.PrintMultipleMemory(userInput)
        elif(memory.CheckIfStoringMemory(userInput)):
            memory.StoreInMemory(userInput)
        elif(memory.CheckIfRunningProgram(userInput)):
            memory.PrintRunningProgram(userInput)
        else:
            memory.ReturningOneMemory(userInput)

sys.exit(0)
