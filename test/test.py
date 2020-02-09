# -*- coding: utf-8 -*-
__date__ = '2020/2/9 17:27'


IP = '127.0.0.1'
PORT = 8888


import socket
import threading

from server.socket_server import TCPSerer
from handler.base_handler import StreamRequestHandler


class TestBaseRequestHandler(StreamRequestHandler):
    """ 测试处理器类 """

    # 具体处理
    def handle(self):
        pass

class SocketServerTest:
    """测试TCPServer"""

    # 开启服务器
    def run_server(self):
        tcp_server = TCPSerer(('127.0.0.1', 8888), TestBaseRequestHandler)  # 创建tcp服务器对象
        tcp_server.serve_forever()  # 启动

    # 具体的客户端连接逻辑
    def client_connect(self):
        client_socket = socket.socket()
        client_socket.connect(('127.0.0.1', 8888))

    # 模拟生成客户端
    def generate_clients(self, num=0):
        clients = []
        for _ in range(num):
            client_thread = threading.Thread(target=self.client_connect)
            clients.append(client_thread)
        return clients

    # 开始模拟测试
    def run(self):
        server_thread = threading.Thread(target=self.run_server)  # 定义服务器线程
        server_thread.start()  # 服务器线程开启

        clients = self.generate_clients(10)
        for client in clients:  # 各个客户端线程开启
            client.start()

        # 等待至线程中止
        server_thread.join()
        for client in clients:
            client.join()


if __name__ == '__main__':
    socket_server_test = SocketServerTest()
    socket_server_test.run()