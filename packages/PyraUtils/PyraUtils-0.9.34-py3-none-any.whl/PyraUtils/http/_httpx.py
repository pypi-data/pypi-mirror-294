# -*- coding: utf-8 -*-

"""
created by：2021-11-25 14:21:41
modify by: 2021-12-02 19:53:33

功能：httpx二次封装，常用的get,post,head,delete方法封装。
     这个是第三方库，使用提前需要pip install httpx

参考文档:
    https://github.com/encode/httpx
    https://www.python-httpx.org/
"""

import httpx
from typing import Union


class HttpxBasicUtil:
    """httpx二次封装，常用的get,post,head,delete等方法封装，工具类。

    注意事项：
    - 初始化超时时间为None时，应使用 httpx.Timeout(None, None)
    使用示例：
    ```python
    resp = HttpxBasicUtil.httpx_method('GET', 'http://example.com')
    ```
    """

    @staticmethod
    def httpx_method(method:str, url:str, **kwargs) -> Union[bytes, str]:
        """Sends a request and returns response content.

        参数:

            method: - ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
            url – 新建 Request 对象的URL
            follow_redirects: 与 requests不同，HTTPX 在默认情况下不遵循重定向。如果需要自动重定向，需要明确执行此操作让"follow_redirects=True".
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
            Response content

        返回类型:
            bytes or str
        """

        try:
            # Client​实例使用 HTTP 连接池。这意味着，当您向同一主机发出多个请求时，​Client​将重用底层 TCP 连接，而不是为每个请求重新创建一个连接。
            with httpx.Client(
                timeout=kwargs.get('timeout'),
                follow_redirects=kwargs.get('follow_redirects', False),
            ) as client:
                resp = client.request(method, url, **kwargs)
                resp.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            raise err
        return resp.content


class HttpxClientUtil:
    """
    
    httpx连接池二次封装，异步支持
    
    常用的get,post,head,delete方法封装，工具类。

    注意事项：
    - 初始化超时时间为None时，应使用 httpx.Timeout(None, None)
    - proxies 参数建议使用字典类型，格式如下：
      {
          "http": "http://user:password@192.168.0.1:8080",
          "https": "https://user:password@192.168.0.1:8080",
      }
    使用示例：
    ```python
    client = HttpxClientUtil(timeout=httpx.Timeout(5.0, connect_timeout=2.0))
    resp = client.httpx_method('GET', 'http://example.com')
    ```
    """

    def __init__(self, http2:bool=False, proxies=None, timeout=5.0,
                max_keepalive=20, max_connections=100, keepalive_expiry:float=5.0) -> None:
        """
        http2: 是否启用 HTTP/2 支持的客户端，默认为 False。
        proxies： 代理地址，建议使用字典格式。可以分别指定 http 和 https 的代理地址。格式如下：
            {
                "http": "http://user:password@192.168.0.1:8080",
                "https": "https://user:password@192.168.0.1:8080",
            }
        max_keepalive : 允许保持活动连接的数量，默认为 20。可以设置为 None 来无限制。
        max_connections: 最大允许连接数，默认为 100。可以设置为 None 来无限制。
        keepalive_expiry: 浮点， 指定连接的存活期限,默认为5.0
        timeout: 超时时间，可以是浮点数或者 None。如果传入 None，则默认禁止超时；如果不是 None，则应该使用 httpx.Timeout 类型。
        """
        self.http2 = http2
        self.proxies = proxies
        self.timeout = httpx.Timeout(timeout) if timeout is not None else httpx.Timeout(None)

        self.limits = httpx.Limits(
            max_keepalive_connections=max_keepalive,
            max_connections=max_connections,
            keepalive_expiry=keepalive_expiry
        )

    def httpx_method(self, method, url, **kwargs) -> httpx.Response:
        """同步方法，使用 httpx.Client 进行请求，在请求完成后自动关闭客户端。"""
        try:
            with httpx.Client(
                http2=self.http2,
                proxies=self.proxies,
                timeout=self.timeout,
                limits=self.limits
            ) as client:
                resp = client.request(method, url, **kwargs)
                resp.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            raise err
        return resp

    async def async_method(self, method, url, **kwargs) -> httpx.Response:
        """异步方法，使用 httpx.AsyncClient 进行请求，在异步操作完成后自动关闭客户端。"""

        try:
            async with httpx.AsyncClient(
                http2=self.http2,
                proxies=self.proxies,
                timeout=self.timeout,
                limits=self.limits
            ) as client:
                resp = await client.request(method, url, **kwargs)
                resp.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            raise err
        return resp
