import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for i in range(1, 100000):
    try:
        s.connect(("172.30.0.4", i))
        print("Open: {}".format(i))
    except Exception as e:
        pass
print("END!")
