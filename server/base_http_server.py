# -*- coding: utf-8 -*-
__date__ = '2020/2/10 21:44'


from server.socket_server import TCPServer


class BaseHTTPServer(TCPServer):

    def __init__(self, server_address=None, handler_class=None):
        super().__init__(server_address, handler_class)

