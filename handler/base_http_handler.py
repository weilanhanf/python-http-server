# -*- coding: utf-8 -*-
__date__ = '2020/2/10 15:51'


import logging


from handler.base_handler import StreamRequestHandler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class BaseHTTPRequestHandler(StreamRequestHandler):
    """ http请求处理 """

    default_http_version = 'HTTP/1.1'

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
            if not self.parse_request():  # 请求解析失败
                return
            # 方法执行get,post
            method_name = 'do_' + self.method
            # 自省检查方法是否存在
            if not hasattr(self, method_name):
                self.write_error(404, None)
                self.send()
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
        # 解析请求行
        first_line = self.read_line()
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

    # 写入应答行：版本，状态码，状态解释等
    def write_response(self, code, msg):
        # 状态行
        response_line = '%s %d %s' % (self.default_http_version, code, msg)
        self.write_content(response_line)
        # 应答头
        # TODO
        self.write_headers('Server', '')
        self.write_headers('Date', '')

    # 写入HTTP
    def write_headers(self, key, value):
        msg = '%s: %s' % (key, value)
        self.write_content(msg)

    # 写入错误HTTP请求的结果，完整封装错误报文
    def write_error(self, code, msg=None):
        short_msg, long_msg = self.responses[code]
        if msg:
            short_msg = msg

        # 错误的html信息
        response_content = self.DEFAULT_ERROR_MESSAGE_TEMPLATE % {
            'code': code,
            'message': short_msg,
            'explain': long_msg,
        }
        # 封装应答消息体
        self.write_response(code, msg)  # 写回错误信息行
        self.end_headers()  # 应答头结束空行
        self.write_content(response_content)  # 写入应答内容

    # 结束应答头
    def end_headers(self):
        self.write_content('\r\n')  # 应答头与应答内容之间有一行空行

    DEFAULT_ERROR_MESSAGE_TEMPLATE = r'''
        <head>
        <title>Error response</title>
        </head>
        <body>
        <h1>Error response</h1>
        <p>Error code %(code)d.
        <p>Message: %(message)s.
        <p>Error code explanation: %(code)s = %(explain)s.
        </body>
        '''

    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
                                               'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }