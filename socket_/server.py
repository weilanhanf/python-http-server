# -*- coding: utf-8 -*-
__date__ = '2020/1/20 9:49'


""" 实现服务端 """


import socket


HOST, PORT = '127.0.0.1', 6666


def server():
    # 创建套接字
    s = socket.socket()
    # 绑定
    s.bind((HOST, PORT))
    # 监听
    s.listen(5)
    # 处理
    while True:  # 利用死循环创建服务器
        c, addr = s.accept()  # 返回客户端连接，连接地址
        print('connect client addr->{}'.format(addr))
        msg = c.recv(1024)
        # print('msg->%s' % msg)
        c.send(msg)


if __name__ == '__main__':
    server()
