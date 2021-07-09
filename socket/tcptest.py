import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("172.19.7.56",8080))
client.connect(("127.0.0.1",8080))
print("服务器说：init")
 
while True:
    info = client.recv(1024)
    print("服务器说：",info.decode("utf-8"))
    # print("服务器说hex：",info.decode("hex"))