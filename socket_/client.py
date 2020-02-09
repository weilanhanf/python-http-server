# -*- coding: utf-8 -*-
__date__ = '2020/1/20 9:49'


""" 实现客户端 """


import socket


HOST, PORT = '127.0.0.1', 6666


def client():
    # 创建套接字
    s = socket.socket()
    # 建立连接
    s.connect((HOST, PORT))
    # 处理信息
    s.send(b' From client: I am client')
    msg = s.recv(1024)
    print('msg from server: %s' % msg)


if __name__ == '__main__':
    client()