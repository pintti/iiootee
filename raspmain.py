import raspbt
from datetime import datetime


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
            #handle data
        #make some wait stuff here this hacked piece of shit right now won't work



if __name__ == "__main__":
    main()
