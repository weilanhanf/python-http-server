# -*- coding: utf-8 -*-
__date__ = '2020/2/9 12:00'
# https://docs.python.org/zh-cn/3/library/socket.html


import threading
import socket


class TCPServer:
    """ 接受客户端的TCP连接 """

    def __init__(self, server_address=None, handler_class=None):
        self.server_address = server_address  # 服务端地址端口
        self.HandlerClass = handler_class  # 网络请求处理器类
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字
        # AF_INET表示一个地址族(ip, 端口号)  SOCK_STREAM表示接收字节流
        self.is_shutdown = False  # 服务器状态，默认停机

    # 服务器启动函数
    def serve_forever(self):
        self.server_socket.bind(self.server_address)  # 绑定地址端口号
        self.server_socket.listen(10)  # 设置最大连接数，超出排队
        # while True:
        while not self.is_shutdown:
            # 1. 接受请求
            request, client_class = self.get_request()
            # 2. 处理请求
            try:  # 捕获处理数据中出现的异常，避免服务器宕机
                # self.process_request(request, client_class)
                self.process_request_multi_thread(request, client_class)  # 多线程处理请求
            except Exception as e:
                print(e)  # 控制台打印查看错误
            # finally:  # 多线程可能请求还未处理完成就关闭连接，所以连接关闭放置在处理请求处理之后
            #     # 3. 关闭连接
            #     self.close_request(request)

    # 接收请求
    def get_request(self):
        return self.server_socket.accept()

    # 处理请求
    def process_request(self, request=None, client_class=None):
        handler = self.HandlerClass(self, request, client_class)  # 处理请求类
        handler.handle()
        # 3. 关闭连接
        self.close_request(request)

    # 多线程处理请求
    def process_request_multi_thread(self, request=None, client_class=None):
        new_thread = threading.Thread(target=self.process_request, args=(request, client_class))
        new_thread.start()

    # 关闭连接
    def close_request(self, request=None):
        request.shutdown(socket.SHUT_WR)
        request.close()

    # 关闭服务器
    def shutdown(self):
        self.is_shutdown = True