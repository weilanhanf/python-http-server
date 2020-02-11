# -*- coding: utf-8 -*-
__date__ = '2020/2/11 12:24'


from handler.simple_http_handler import SimpleHTTPRequestHandler
from server.base_http_server import BaseHTTPServer


class SimpleHTTPServer(BaseHTTPServer):
    """ 简易http服务器 """
    def __init__(self, server_address=None, handler_address=None):
        super().__init__(server_address, handler_address)
        self.version = 'version0.1'
        self.server_name = 'SimpleHTTPServer'


if __name__ == '__main__':
    SimpleHTTPServer(('127.0.0.1', 8888), SimpleHTTPRequestHandler).serve_forever()