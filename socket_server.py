#socket服务端
import socket
import threading #多线程连接库
server = socket.socket() #套接字
#绑定ip和端口
server.bind(('0.0.0.0',8000))
#监听端口
server.listen()
# 定义一个方法来获取值给线程使用
def handle_sock(sock, addr):
    while True:
        sock.send("welcome to server!".encode("utf8"))
        tmp_data = sock.recv(1024)
        print("client respones:{}".format(tmp_data.decode("utf8")))
        intput_data = input()
        sock.send(intput_data.encode("utf8"))
#获取客户端连接并启动线程进行处理，实现多线程
while True:
    #阻塞等待用户连接   每个用户都要分配一个地址
    sock, addr = server.accept()
    # 启动一个线程去处理新用户连接 传进来的是一个方法名，不是方法
    client_thread = threading.Thread(target = handle_sock,args = (sock, addr))#一个新线程产生所做的操作；
    client_thread.start()

# 体验裸数据的获取，数据没有进行包装时候的处理过程，上面用方法实现了多线程的连接，多线程连接只用客户端定义就行；
# 注意的是上面定义的方法传入的是方法名而不是方法；
# Python中循环函数的使用和其他软件的差异性要懂；
#



