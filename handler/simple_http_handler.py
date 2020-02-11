# -*- coding: utf-8 -*-
__date__ = '2020/2/11 11:09'


import os
from urllib import parse

from handler.base_http_handler import BaseHTTPRequestHandler


RESOURCES_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                              '../resources')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, server_socket=None, request=None, client_address=None):
        super().__init__(server_socket, request, client_address)

    def get_resource(self, path):
        # 解析路径
        url_result = parse.urlparse(path)
        recourse_path = str(url_result[2])
        if recourse_path.startswith('/'):  # 截取资源
            recourse_path = recourse_path[1:]
        recourse_path = os.path.join(RESOURCES_PATH, recourse_path)  # 拼接资源绝对路径
        # 判断资源是否存在并返回
        if os.path.exists(recourse_path) and os.path.isfile(recourse_path):
            return True, recourse_path
        else:
            return False, recourse_path

    def do_GET(self):
        found, recourse_path = self.get_resource(self.path)  # 请求资源解析结果
        # print(found, recourse_path)
        if not found:  # 如果未找到解析结果，返回404错误
            self.write_error(404)
            self.send()
        else:
            # 打开文件，并获取文件长度
            with open(recourse_path, 'rb') as f:
                fs = os.fstat(f.fileno())
                file_length = str(fs[6])  # 文件字节为单位的长度
                # 写入响应行和响应头中长度
                self.write_response(200)  # 响应状态行成功200
                self.write_headers('Content-Length', file_length)  # 写入响应头
                self.end_headers()  # 响应头与响应内容之间换行
                # 文件读入缓存区并写入响应信息内容
                while True:
                    buf = f.read(1024)  # 读取1024个字节
                    if not buf:  # 文件读取结束跳出循环
                        break
                    else:
                        self.write_content(buf)
    # 实现post方法：验证账号密码
    def do_POST(self):
        pass

