#socket客户端
import socket
client = socket.socket() # 新建套接字
client.connect(('172.30.62.10',8000)) #建立一个连接
# 写一个接收函数
server_data =  client.recv(1024);
print("server respones: {}".format(server_data.decode("utf8")))
while True:
    # tem_data = client.recv(1024)
    # if tem_data:
    #     data += tem_data.decode("utf8")
    # else:
    #     break;
    input_data = input()
    client.send(input_data.encode("utf8"))
    server_data = client.recv(1024)
    print("server respones: {}".format(server_data.decode("utf8")))
# client.close()
