import raspbt
from datetime import datetime

MEMORY_PATH = "memory.csv"

def memory_manage(path):
    try:
        with open(path, "r") as memory:
            content = memory.readlines()
        if len(content) > 48:
            content = content[-25:-1]
        with open(path, "w") as memory:
            memory.write(content)
    except FileNotFoundError or PermissionError:
        print("Error when opening memory file!")
        pass

def main():
    timeUntilSync = 0
    timeWait = 0
    while True:
        timeNow = datetime.timestamp(datetime.now())
        if int(timeUntilSync - timeNow) != timeWait:
            timeWait = int(timeUntilSync - timeNow)
            print(timeWait)
        if timeUntilSync - timeNow < 0: 
            data, lastTime = raspbt.main()
            print(data, lastTime)
            timeUntilSync = datetime.timestamp(lastTime)
            print("timeuntil sync ", timeUntilSync-timeNow)
            memory_manage(MEMORY_PATH)
            raspbt.data_to_memory(data)
        #make some wait stuff here this hacked piece of shit right now won't work



if __name__ == "__main__":
    main()
