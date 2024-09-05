# -*- coding: utf-8 -*-

import hmac

class HmacUtil:
    @staticmethod
    def sign(key:bytes, msg:bytes=None, digestmod:str='sha256'):
        """
        使用指定的哈希算法创建一个 HMAC 签名。

        :param key: 密钥，用于HMAC算法的密钥。必须是 bytes 或 bytearray 类型。
        :param msg: 要签名的消息，如果提供了该参数，则必须是 bytes、bytearray 或者 memoryview 类型。默认为 None。
        :param digestmod: 指定用于HMAC的哈希算法名称的字符串，默认为 'sha256'。
                        支持 hashlib 支持的所有算法，以及 OpenSSL 库可能提供的其他算法。
                        常见的哈希算法包括但不限于：
                        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                        'blake2b', 'blake2s',
                        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                        'shake_128', 'shake_256'。

        :return: 签名结果的十六进制字符串形式，经过 utf-8 编码转换为 bytes 对象。

        HMAC 签名用于数据认证，确保数据在传输或存储过程中未被篡改。选择合适的哈希算法可以根据安全需求和性能要求进行权衡。

        注意：hashlib 的构造器（例如 hashlib.sha256()）通常比对应的 new() 方法（例如 hashlib.new('sha256')）
            更快，因此当可用时应优先使用。

        示例:
            # 密钥和消息都需要为 bytes 类型
            secret_key = b'secret'
            message = b'Some important data'

            signature = sign(secret_key, message)
            print(signature)  # 输出类似 '89a...ef' 这样的签名字符串

        """
        if not isinstance(key, (bytes, bytearray)):
            raise ValueError("Key must be bytes or bytearray.")
        
        if msg is not None and not isinstance(msg, (bytes, bytearray, memoryview)):
            raise ValueError("Message must be bytes, bytearray, or memoryview if provided.")
        
        try:
            # 使用 hmac 模块和指定的哈希方法来创建新的HMAC对象
            h = hmac.new(key, msg=msg, digestmod=digestmod)
            
            # 返回十六进制表示的HMAC签名，并转换成bytes类型
            return h.hexdigest().encode('utf-8')
        except ValueError as e:
            raise ValueError(f"Invalid digest mode: {digestmod}. Please check the supported algorithms.")

    @staticmethod
    def verify(a, b):
        """
        安全地比较两个HMAC摘要值是否相等。

        :param a: 第一个比较值，可为bytes或ASCII字符串（如hashlib的hexdigest()结果）
        :param b: 第二个比较值，类型必须与a相同

        :return: 布尔值，如果两个值相等返回True，否则返回False

        使用 hmac 模块的 compare_digest 函数来进行比较防止定时攻击。这是因为 compare_digest 设计上
        会以恒定时间运行，不管输入值的大小或内容。这种方法能有效降低通过时间分析差异来猜测信息的可能性，
        从而提高安全性。
        
        对于比较敏感数据（如密码、密钥等）时，应该使用本函数而非简单的 == 运算符，
        因为 == 运算符可能引入基于内容的短路行为，增加信息泄露风险。

        示例:
            valid = verify(hmac_signature, expected_signature)
            if valid:
                print("验证成功，数据未被篡改。")
            else:
                print("验证失败，数据可能已被篡改。")

        注意：为保证函数正确运作，传入的 a 和 b 必须是同样的类型，并且对于文本类比较，
            应只包含ASCII字符。

        """
        if not (isinstance(a, (bytes, str)) and isinstance(b, (bytes, str))):
            raise ValueError("Both a and b must be bytes or ASCII strings.")

        try:
            # 使用 hmac 模块中的 compare_digest 函数进行安全比较
            return hmac.compare_digest(a, b)
        except TypeError as e:
            raise TypeError(f"Error in HMAC comparison: {e}")
            