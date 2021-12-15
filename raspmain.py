import raspbt
from datetime import date, datetime
import time

MEMORY_PATH = ""

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
    except (FileNotFoundError, PermissionError):
        print("Error when opening memory file!")


#Take list of two values and write into file with csv format
def data_to_memory(data):
    try:
        with open(f"{MEMORY_PATH}", "a+") as memfile:
            hour = get_hour()
            memfile.write(f"{hour}: {data[0]},{data[1]}\n")
    except (FileNotFoundError, PermissionError):
        print("Error when writing memory file!")


def get_date():
    return datetime.now().date()


def get_hour():
    return datetime.now().hour


def update_memory_path():
    global MEMORY_PATH
    MEMORY_PATH = "temp/" + str(get_date()) + ".txt"


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
                update_memory_path()
                #memory_manage(MEMORY_PATH)
                data_to_memory(data)
                timeUntilSync = raspbt.main_sleep(sock)
        except UnicodeDecodeError:
            print("Small unicode error, retrying")


if __name__ == "__main__":
    main()
