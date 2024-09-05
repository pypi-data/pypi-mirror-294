# -*- coding: utf-8 -*-

"""
created by：2017-05-10 20:11:31
modify by: 2024-03-07 23:21:32

功能：requests二次封装，常用的get,post,head,delete方法封装。
     这个是第三方库，使用提前需要pip install requests

参考文档:
    http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
    http://docs.python-requests.org/zh_CN/latest/user/advanced.html
    http://docs.python-requests.org/zh_CN/latest/api.html
    http://docs.python-requests.org/zh_CN/latest/_modules/requests/api.html
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RequestsBasiceUtil:
    """requests二次封装，常用的get,post,head,delete方法封装，工具类。"""

    @staticmethod
    def req_method(method:str, url:str, **kwargs) -> requests.Response:
        """Sends request.

        参数:

            method: - ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
            url – 新建 Request 对象的URL
            params – (可选) Request 对象的查询字符中要发送的字典或字节内容
            data – (可选) Request 对象的 body 中要包括的字典、字节或类文件数据
            json – (可选) Request 对象的 body 中要包括的 Json 数据
            headers – (可选) Request 对象的字典格式的 HTTP 头
            cookies – (可选) Request 对象的字典或 CookieJar 对象
            files – (可选)字典，'name':file-like-objects(或{'name':('filename',fileobj)})用于上传含多个部分的（类）文件对象
            auth – (可选) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
            timeout (浮点或元组) – (可选) 等待服务器数据的超时限制，是一个浮点数，或是一个(connect timeout, read timeout)元组
            allow_redirects (bool) – (可选) Boolean. True 表示允许跟踪 POST/PUT/DELETE 方法的重定向
            proxies – (可选) 字典，用于将协议映射为代理的URL
            verify – (可选) 为 True 时将会验证 SSL 证书，也可以提供一个 CA_BUNDLE 路径
            stream – (可选) 如果为 False，将会立即下载响应内容
            cert – (可选) 为字符串时应是 SSL 客户端证书文件的路径(.pem格式)，如果是元组，就应该是一个(‘cert’, ‘key’) 二元值对

        返回:
            Response object

        返回类型:
            requests.Response
        """
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
        except (requests.ConnectionError,
                requests.HTTPError,
                requests.Timeout,
                requests.URLRequired) as err:
            raise RuntimeError(f"请求出错: {err}")
        return resp

class RequestsSessionUtil:
    """
    封装 requests.Session 类，提供连接池和持久化功能。
    """

    def __init__(self, retries: int = 5, backoff_factor: float = 0.3,
                 status_forcelist: list = [500, 502, 503, 504],
                 session: requests.Session = None):
        """
        初始化 Session，并配置重试策略。

        参数：
            retries: 最大重试次数。
            backoff_factor: 退避因子，决定睡眠时间。
            status_forcelist: 需要触发重试的状态码列表。
            session: 如果提供，则使用该 session，否则创建新的 session。
        """
        self.session = session or requests.Session()
        retry_strategy = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def session_method(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        使用预配置的 Session 来发送请求。

        参数：
            method: HTTP 请求方法，如 'GET', 'POST' 等。
            url: 请求的 URL。
            **kwargs: requests.Session.request 方法所接受的其他参数。

        返回:
            Response object.
        """
        response = self.session.request(method, url, **kwargs)
        return response
