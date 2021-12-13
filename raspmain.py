import raspbt
from datetime import datetime
import time

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


#Take list of two values and write into file with csv format
def data_to_memory(data):
    try:
        with open("memory.csv", "a") as memfile:
            memfile.write(f"{data[0]},{data[1]}\n")
    except FileNotFoundError or PermissionError: 
        print("Error when reading memory file!")
        pass


def main():
    timeUntilSync = 0
    timeWait = 0
    startTime = 0
    while True:
        try:
            timeNow = time.time() - startTime
            if int(timeUntilSync - timeNow) != timeWait:
                timeWait = int(timeUntilSync - timeNow)
                print(timeWait)
            if timeUntilSync - timeNow < 0: 
                data, sock = raspbt.main_data()
                startTime = time.time()
                memory_manage(MEMORY_PATH)
                data_to_memory(data)
                timeUntilSync = raspbt.main_sleep(sock)
        except UnicodeDecodeError:
            print("Small unicode error, retrying")


if __name__ == "__main__":
    main()
