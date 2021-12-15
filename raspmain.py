import raspbt
from datetime import date, datetime
import time

memory_path = ""

#Take list of two values and write into file with format->  HH: OO.OO,II.II\n
def data_to_memory(data):
    try:
        with open(f"{memory_path}", "a+") as memfile:
            hour = get_hour()
            memfile.write(f"{hour}: {data[0]},{data[1]}\n")
    except (FileNotFoundError, PermissionError):
        print("Error when writing memory file!")


def get_date():
    return datetime.now().date()


def get_hour():
    return datetime.now().hour


def update_memory_path():
    global memory_path
    memory_path = "temp/" + str(get_date()) + ".txt"


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
                data_to_memory(data)
                timeUntilSync = raspbt.main_sleep(sock)
        except UnicodeDecodeError:
            print("Small unicode error, retrying")


if __name__ == "__main__":
    main()
