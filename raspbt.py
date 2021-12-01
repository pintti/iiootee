import bluetooth as bt, time

btAddr = '91:EB:E9:EC:B6:01'

def recv(sock):
    try:
        data = sock.recv(1024)
        print(data)
        return data
    except:
        print("Receive failed")
        return


def btConnect(address):
    start = time.time()
    while time.time()-start < 10: #this might need to be longer
        try:
            sock = bt.BluetoothSocket(bt.RFCOMM)
            sock.connect((address, 1))
            return sock
        except:
            print("Connection failed, trying again")
    print("Timed out")
    return


def syncClock(sock):
    try:
        clock = time.time()
        sock.send(clock[3])
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
    start = time.time()
    while time.time()-start<10:
        sock.send((1).to_bytes(1, "big"))
        ack = sock.recv(1024).decode().strip()
        print(ack)
        if ack == "1":
            return True
    print("ACK failed")
    return False


def main():
    sock = btConnect(btAddr)
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
