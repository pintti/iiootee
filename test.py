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
        return temp[0].split(","), False
    else:
        return temp[0].split(","), ACK


print(handle_data(b'21.31,20.50\r\n'))