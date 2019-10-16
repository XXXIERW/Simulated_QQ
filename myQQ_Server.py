import socket
import threading # 线程配置
import json # 消息格式为JSON，引用JSON方法
from collections import  defaultdict

# 维护用户连接
online_users = defaultdict(dict) # 初始化一个用户连接，没有数据的时候传入一个空值
# 维护用户的历史消息
user_msgs = defaultdict(list) # 消息不止一条用列表列出

server = socket.socket();

# 绑定一个ip
server.bind(("0.0.0.0",8000))
server.listen()

# 定义一个连接配置
def handle_sock(sock, addr):
    while True:
        tmp_data = sock.recv(1024) # 拿到所有传入的最大值
        json_data = json.loads(tmp_data.decode("utf8")) # 将str类型转为dict
        action = json_data.get("action","") # 拿到用户一个状态值，来判断用户操作
        if action == "login":
            # 将用户数据传入到dict里面存储起来，向连接发送数据
            online_users[json_data["user"]] = sock
            sock.send("用户登录成功！".encode("utf8"))
        # 获取在线用户
        elif action == "list_user":
            # item() 方法以列表返回可遍历的(键, 值) 元组数组。 拿到所有在线用户 ，在将sock加入到在线用户中
            all_onlineUser = [user for user, sock in online_users.items()]
            #  json.dumps()用于将dict类型的数据转成str 强制转换， 传给客户端
            sock.send(json.dumps(all_onlineUser).encode("utf8"))
        #  获取历史消息
        elif action == "history_msg":
            # 通过用户名获取获取到用户消息，无消息则传回空值，利用GET的方法来获取
            sock.send(json.dumps(user_msgs.get(json_data["user"],[])).encode("utf8"))
        # 发送消息  首先获取用户的sock来进行用户的传送  发送消息给在线用户
        elif action == "send_msg":
            if json_data["to"] in online_users:
                online_users[json_data["to"]].send(json.dumps(json_data).encode("utf8"))
            user_msgs[json_data["to"]].append(json_data)# 将值附加给json_data
        # 用户退出
        elif action == "exit":
            del online_users[json_data["user"]]
            sock.send("退出成功！".encode("utf8"))
# 启动一个阻塞来等待连接 启动线程来做多线程配置
while True:
    sock, addr = server.accept() #阻塞等待用户连接
    client_thread = threading.Thread(target=handle_sock, args=(sock,addr))# 利用多线程进行用户的操作，
    client_thread.start() # 启动线程连接

# 多线程去处理每个用户连接，防止主线程阻塞住
# 自定义消息协议并且完成消息协议的解析