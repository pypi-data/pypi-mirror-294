
import os
import datetime
from OpenSSL import crypto

class CheckSSLCert:
    @staticmethod
    def is_pem_format(cert_path):
        """
        检查给定路径的证书文件是否为有效的PEM格式。

        :param cert_path: 证书文件的路径。
        :return: 布尔值，表示是否为有效的PEM格式
        """
        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"证书文件不存在: {cert_path}")

        try:
            with open(cert_path, 'rb') as cert_file:
                cert_content = cert_file.read()
            # 尝试加载证书内容
            crypto.load_certificate(crypto.FILETYPE_PEM, cert_content)
            return True
        except crypto.Error:
            # 如果加载失败，则不是有效的PEM格式
            return False

    @staticmethod
    def check_ssl_cert_expiry(cert_path, days=30):
        """
        检查给定路径的 SSL 证书是否将在指定天数内过期。

        :param cert_path: 包含 SSL 证书的路径。
        :param days: 相对于当前日期，考虑为即将过期的天数阈值。
        :return: 元组 (即将过期的布尔值, 证书开始日期, 错误信息)
        """
        if not os.path.exists(cert_path):
            return False, None, f"证书文件不存于路径 {cert_path}"

        try:
            # 读取证书内容
            with open(cert_path, 'rb') as cert_file:
                cert_content = cert_file.read()

            # 加载证书
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_content)

            # 获取证书创建时间
            before_date = datetime.datetime.strptime(cert.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        
            # 获取证书过期时间
            expiration_date = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
            # 计算当前时间与过期时间的差值
            remaining = expiration_date - datetime.datetime.utcnow()

            # 判断是否快到期
            return remaining < datetime.timedelta(days=days), before_date, None
        except Exception as e:
            return False, None, str(e)
