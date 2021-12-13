import raspbt
from datetime import datetime

MEMORY_PATH = "memory.csv"

def memory_manage(path):
    new_content = []
    try:
        with open(path, "r") as memory:
            content = memory.readlines()
        if len(content) > 48:
            content = content[-25:-1]
        for line in content:
            new_line = line.rstrip("\n")
            if len(new_line) > 0:
                new_content.append(new_line)
        with open(path, "w") as memory:
            memory.write("\n".join(new_content))
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
