#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
此模块提供了解析SSL证书的工具类。支持PEM和DER两种编码格式的证书。

文档参考:
- https://stackoverflow.com/questions/16899247/how-can-i-decode-a-ssl-certificate-using-python
- https://cryptography.io/en/latest/x509/reference/
"""

import ssl
import socket
from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class CertUtils:
    """
    SSL证书实用工具类。
    
    该类包括以下方法：
    - 从本地文件读取SSL证书信息。
    - 使用OpenSSL库转换和解码证书内容。
    - 使用cryptography库转换和解码证书内容。
    - 通过建立网络连接获取特定服务器SSL证书信息。
    """

    def __init__(self):
        """
        初始化CertUtils实例。
        """
        # 此函数不需要执行任何操作，因为没有初始化参数或者实例变量。
        pass

    def get_ssl_file_info(self, cert_file):
        """
        读取指定路径的证书文件，并以字典的形式返回证书信息。
        
        Args:
            cert_file (str): SSL证书文件的文件路径。

        Returns:
            dict: 包含证书各字段信息的字典。

        Raises:
            RuntimeError: 如果无法读取证书，抛出运行时错误。
        """
        try:
            ssl_info = ssl._ssl._test_decode_cert(cert_file)
        except ssl.SSLError as err:
            raise RuntimeError(f'无法读取证书 {cert_file}: {err}')
        return ssl_info

    def load_x509_cert_use_openssl(self, cert_data: bytes, cert_format="pem"):
        """
        使用OpenSSL库将证书数据转成X.509对象，并返回其文本输出。

        Args:
            cert_data (bytes): 包含证书原始数据的字节数组。
            cert_format (str): 指定证书格式，可以是"pem"或"der"。

        Returns:
            bytes: 返回证书的文本表示形式。

        Raises:
            AssertionError: 如果输入的不是字节序列，则抛出断言错误。
        """
        assert isinstance(cert_data, bytes), '证书数据必须是字节序列。'
         # 根据提供的证书格式，使用合适的文件类型常量加载证书
        file_type = crypto.FILETYPE_ASN1 if cert_format == "der" else crypto.FILETYPE_PEM
        # 使用OpenSSL库加载证书数据，返回一个X.509证书对象
        cert_X509 = crypto.load_certificate(file_type, cert_data)
        # 将X.509证书对象转储为人类可读的文本形式，并返回该字节序列
        cert_x509_data = crypto.dump_certificate(crypto.FILETYPE_TEXT, cert_X509)
        return cert_x509_data

    def load_x509_cert_use_cryptography(self, cert_data: bytes, cert_format="pem"):
        """
        使用cryptography库将证书数据转成证书对象。

        Args:
            cert_data (bytes): 包含证书数据的字节序列。
            cert_format (str): 指明所用的证书格式："pem" 或 "der"。

        Returns:
            Certificate: 包含转换后的证书对象。

        Raises:
            AssertionError: 如果输入的不是字节序列，则抛出断言错误。
        """
        assert isinstance(cert_data, bytes), '证书数据必须是字节序列。'
        if cert_format == "der":
             # 如果证书格式为DER，则使用load_der_x509_certificate方法加载
            return x509.load_der_x509_certificate(cert_data, default_backend())
        else:
            # 如果证书格式不是DER（默认为PEM），则使用load_pem_x509_certificate方法加载
            return x509.load_pem_x509_certificate(cert_data, default_backend())

    def get_ssl_url_info(self, hostname: str, port=443) -> dict:
        """
        连接指定主机名和端口的服务器，获取SSL证书信息。

        Args:
            hostname (str): 服务器域名或IP地址。
            port (int): 连接端口，默认为443。

        Returns:
            dict: 解析的证书信息字典。

        Raises:
            RuntimeError: 如果无法建立连接或检索SSL信息，将抛出运行时错误。
        """
        context = ssl.create_default_context()
        # 创建一个包装有SSL上下文的socket。
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)

        try:
            conn.settimeout(3.0)  # 设置超时为3秒
            conn.connect((hostname, port))  # 建立连接
            ssl_info = conn.getpeercert()   # 获取对等SSL证书
        except (ssl.SSLCertVerificationError, socket.timeout) as err:
            raise RuntimeError(f'连接或验证失败: {err}')
        finally:
            conn.close()  # 关闭连接
        return ssl_info
