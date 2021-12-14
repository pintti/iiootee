import bluetooth as bt #pybluez
import datetime

btAddr = '91:EB:E9:EC:B6:01'
LAST_SYNC: datetime.datetime = None


def get_current_time():
    return datetime.datetime.now()


def get_current_timestamp():
    return get_current_time().timestamp()


def update_last_sync(sync_time: datetime.datetime):
    global LAST_SYNC
    LAST_SYNC = sync_time


def recv(sock):
    try:
        data = sock.recv(1024)
        print(data)
        return data
    except:
        print("Receive failed")
        return None


def btConnect(address):
    start = get_current_timestamp()
    while get_current_timestamp() - start < 10:
        try:
            sock = bt.BluetoothSocket(bt.RFCOMM)
            sock.connect((address, 1))
            return sock
        except:
            print("Connection failed, trying again")
    print("Timed out")
    return


def sync_with_arduino(sock: bt.BluetoothSocket, seconds_to_transfer: int):
    timeout_seconds = 10
    print(int(seconds_to_transfer))
    # Send future timestamp when next temperature should be coming from Arduino
    sock.send(int(seconds_to_transfer).to_bytes(2, "big"))
    _, ack = handle_data(recv(sock))
    sync_start = get_current_timestamp()
    while get_current_timestamp() - sync_start < timeout_seconds:
        if ack == "1":
            return True
        _, ack = handle_data(recv(sock))

    print(f"Sync failed after waiting {timeout_seconds} seconds")
    return False


def syncClock(sock):
    try:
        print("Sync clock")
        remaining_seconds = seconds_till_hour()
        success = sync_with_arduino(sock, remaining_seconds)
        if not success:
            raise TimeoutError("Sync with Arduino failed")
        update_last_sync(remaining_seconds)
        return True
    except:
        print("Clock sync failed")
        return False


def handle_data(data):
    temp = 0
    ACK = False
    temperature = []
    data = data.decode().strip().split()
    if len(data)>1:
        temp = data[0]
        ACK = data[1]
    else:
        temp = data
    if not ACK:
        return temp.split(","), False
    else:
        return temp.split(","), ACK


def seconds_till_hour():
    currentTime = get_current_time()
    delta = datetime.timedelta(hours=1)
    nextHour = (currentTime + delta).replace(microsecond=0, second=0, minute=2)
    secondsToWait = (nextHour - currentTime).seconds
    return secondsToWait


def main_data():
    sock = btConnect(btAddr)
    if sock:
        while True:
            data = recv(sock)
            data, ACK = handle_data(data)
            if data:
                print(data)
                return data, sock
    else:
        print("Program failed")
        return 1


def main_sleep(sock):
    for i in range(0, 10):
        if sock:
            print("Starting sleep sync")
            if syncClock(sock):
                sock.close()
                return LAST_SYNC


if __name__ == "__main__":
    main_data()
