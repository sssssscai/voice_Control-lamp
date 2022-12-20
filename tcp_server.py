# 导入socket模块
import socket

if __name__ == '__main__':
    # 创建tcp服务端套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置端口号复用，让程序退出端口号立即释放
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # 给客户端绑定端口号，客户端需要知道服务器的端口号才能进行建立连接。IP地址不用设置，默认就为本机的IP地址。
    tcp_server.bind(("", 51234))

    # 设置监听
    # 128:最大等待建立连接的个数
    tcp_server.listen(128)

    # 等待客户端建立连接的请求, 只有客户端和服务端建立连接成功代码才会解阻塞，代码才能继续往下执行
    # 1. 专门和客户端通信的套接字： tcp_client
    # 2. 客户端的ip地址和端口号： tcp_client_address
    tcp_client1, tcp_client_address1 = tcp_server.accept()
    tcp_client2, tcp_client_address2 = tcp_server.accept()
    
    print("灯泡的ip地址和端口号:", tcp_client_address1)
    recv_data = tcp_client1.recv(1024)
    recv_content = recv_data.decode(encoding="utf-8")
    print("灯泡客户端的数据为:", recv_content)

    print("主机的ip地址和端口号:", tcp_client_address2)
    recv_data = tcp_client2.recv(1024)
    recv_content = recv_data.decode(encoding="utf-8")
    print("主机客户端的数据为:", recv_content)
    #发送灯泡ip地址以及端口给客户端
    t=tcp_client_address1[0]+" "+str(tcp_client_address1[1])
    send_data = t.encode(encoding="utf-8")
    tcp_client2.send(send_data)
    
    while True:
        recv_data = ""
        #接收客户端控制信号
        while True:
            try:
                recv_data = tcp_client2.recv(1024)
                break
            except ConnectionResetError:
                print("用户客户端已近断开，正在等待重新连接...")
                tcp_client2, tcp_client_address2 = tcp_server.accept()
                print("用户客户端连接成功")
                print("用户客户端的ip地址和端口号:", tcp_client_address2)
                t=tcp_client_address1[0]+" "+str(tcp_client_address1[1])
                send_data = t.encode(encoding="utf-8")
                tcp_client2.send(send_data)

        recv_content = recv_data.decode(encoding="utf-8")
        #发送控制信号给esp8266
        x = recv_content
        send_data = x.encode(encoding="utf-8")

        while True:
            try:
                tcp_client1.send(send_data)
                break
            except ConnectionResetError:
                print("灯泡连接断开，正在等待重新连接...")
                tcp_client1, tcp_client_address1 = tcp_server.accept()
                print("灯泡重新连接成功")
                print("灯泡的ip地址和端口号:", tcp_client_address1)
    
    tcp_client.close()
