# -*- coding: utf-8 -*-
__date__ = '2020/2/9 15:59'


class BaseRequestHandler:
    """ 请求处理基类：定义基本属性接口 """

    def __init__(self, server_socket=None, request=None, client_address=None):
        self.server_socket = server_socket
        self.request = request
        self.client_address = client_address

    def handle(self):
        # raise Exception("This method need be overridden")
        pass


class StreamRequestHandler(BaseRequestHandler):
    """ 网络请求处理器类：封装TCP连接处理逻辑，编码解码，读写消息"""

    def __init__(self, server_socket=None, request=None, client_address=None):
        super().__init__(server_socket, request, client_address)
        self.buff = []  # 设置缓冲区
        # 把连接请求分离为读和写文件描述符
        self.readfile = self.request.makefile("rb")
        self.writefile = self.request.makefile("wb")

    # 编码：字符串->字节流
    def encode(self, msg=None):
        if not isinstance(msg, bytes):  # 如果不是字节码，编码为字节码
            msg = bytes(msg, encoding='utf-8')
        return msg

    # 解码：字节流->字符串
    def decode(self, msg=None):
        if isinstance(msg, bytes):  # 把字节码解码为字符串
            msg = msg.decode()
        return msg

    # 读消息
    def read(self, length=0):
        msg = self.readfile.read(length)  # 指定读取一定长度的消息
        return self.decode(msg)  # 返回解码后的字符串

    # 读取一行消息
    def read_line(self, length=65536):  # 浏览器能够处理的请求的大小默认值length
        msg = self.readfile.readline(length).strip()
        return self.decode(msg)

    # 写消息
    def write_content(self, msg):
        msg = self.encode(msg)
        self.buff.append(msg)  # 数据写回缓冲区

    def send(self):
        for line in self.buff:  # 读取缓冲区
            self.writefile.write(line)
        self.writefile.flush()  # 所有缓存数据强发送到目的地
        self.buff = []  # 缓存区清空

    # 关闭文件描述符
    def close(self):
        self.readfile.close()
        self.writefile.close()
