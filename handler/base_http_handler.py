# -*- coding: utf-8 -*-
__date__ = '2020/2/10 15:51'


import logging


from handler.base_handler import StreamRequestHandler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class BaseHTTPRequestHandler(StreamRequestHandler):
    """ http请求处理 """

    def __init__(self, server_socket=None, request=None, client_address=None):
        super().__init__(server_socket, request, client_address)
        self.headers = None
        self.path = None
        self.version = None
        self.method = None
        self.body = None

    # 处理请求
    def handle(self):
        try:
            # 解析请求
            if not self.parse_request(): # 请求解析失败
                return
            # 方法执行
            method_name = 'do_' + self.method
            # 自省检查方法是否存在
            if not hasattr(self, method_name):
                # TODO 请求消息发送错误
                return
            method = getattr(self, method_name)
            method()  # 对应答报文的封装
            # 消息发送结束
            self.send()
        except Exception as e:
            logging.exception(e)

    # 解析请求头
    def parse_headers(self):
        headers = {}
        while True:
            line = self.read_line()  # 逐行读取
            if line:
                key, value = line.split(':', 1)  # 请求头逐行拆分键值对
                key, value = key.strip(), value.strip()  # 去掉前后多余空格
                headers[key] = value  # 加入解析头
            else:
                break
        return headers

    # 解析请求
    def parse_request(self):
        try:
            # 解析请求行
            first_line = self.readfile.readline()
            words = first_line.split()  # 把请求行按空格拆分
            self.method, self.path, self.version = words  # 获取请求方法，路径，版本

            # 解析请求头
            self.headers = self.parse_headers()

            # 解析请求内容
            key = 'Content-Length'
            if key in self.headers.keys():  # 如果请求内容不为空
                body_length = int(self.headers[key])  # 从保存的请求头中取得请求体长度
                self.body = self.read(body_length)  # 读取请求内容

            return True  # 解析请求成功

        except Exception:
            return False