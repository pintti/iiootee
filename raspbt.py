import bluetooth as bt
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
    while get_current_timestamp() - start < 10: #this might need to be longer
        try:
            sock = bt.BluetoothSocket(bt.RFCOMM)
            sock.connect((address, 1))
            return sock
        except:
            print("Connection failed, trying again")
    print("Timed out")
    return


def sync_with_arduino(sock: bt.BluetoothSocket, sync_time: datetime.datetime):
    timeout_seconds = 10
    # Send future timestamp when next temperature should be coming from Arduino
    sock.send(int(sync_time.timestamp()).to_bytes(4, "big"))
    ack = recv(sock).decode().strip()

    sync_start = get_current_timestamp()
    while get_current_timestamp() - sync_start < timeout_seconds:
        if ack == "1":
            return True
        ack = recv(sock).decode().strip()
    
    print(f"Sync failed after waiting {timeout_seconds} seconds")
    return False


def syncClock(sock):
    try:
        remaining_seconds = (LAST_SYNC + datetime.timedelta(minutes=10)).timestamp() - get_current_timestamp()
        future_time = get_current_time() + datetime.timedelta(seconds=remaining_seconds)
        success = sync_with_arduino(sock, future_time)
        if not success:
            raise TimeoutError("Sync with Arduino failed")
        update_last_sync(future_time)
    except:
        print("Clock sync failed")


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
    t = ""
    for s in temp:
        if s != ',':
            t += s
        else:
            temperature.append(t)
            t = ""
    temperature.append(t)
    if not ACK:
        return temperature, False
    else:
        return temperature, ACK


def comAck(sock):
    start = get_current_timestamp()
    while get_current_timestamp() - start < 10:
        sock.send((1).to_bytes(1, "big"))
        ack = recv(sock).decode().strip()
        print(ack)
        if ack == "1":
            return True
    print("ACK failed")
    return False


def main():
    sock = btConnect(btAddr)
    update_last_sync(get_current_time())
    if sock:
        while True:
            data = recv(sock)
            data, ACK = handle_data(data)
            if data:
                print(data)
                print("Starting ACK")
                if comAck(sock):
                    print("ACK works")
                    #time.sleep(590)
                    #
                    #make return here for master


    else:
        print("Program failed")
        return 1

if __name__ == "__main__":
    main()
