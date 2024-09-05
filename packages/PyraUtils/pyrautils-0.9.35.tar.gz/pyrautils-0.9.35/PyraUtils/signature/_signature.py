#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by: 2018-4-16 20:59:0
modify by: 2023-05-25 11:24:33

功能：generate nonce or signature
"""

import uuid
import random
import hmac
import hashlib
import base64
import secrets

class GenerateNonceUtil:
    """Generate Nonce utility class."""

    def gen_nonce_use_random(self, length=8):
        """
        使用 random 模块生成一个伪随机数作为随机值。
        
        :param length: 生成的随机数长度，默认为8位。
        :return: 返回由随机数字组成的字符串。
        """
        # 使用列表解析式生成指定长度的随机数，并转换为字符串返回
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def gen_nonce_use_secrets(self, length=8):
        """
        使用 secrets 模块生成加密安全强度的随机字符串。
        
        :param length: 生成的随机字符串长度，默认为8位。
        :return: 返回由随机字符组成的字符串，字符集包括数字和字母。
        """
        # 定义符合要求的字符集合
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # 利用 secrets.choice() 随机选择字符构造随机字符串并返回
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def gen_nonce_use_uuid1(self):
        """
        使用 uuid 模块的 uuid1 函数生成基于主机ID和当前时间的唯一键。
        
        :return: 基于UUID1算法生成的独特标识符的字符串形式。
        """
        # 直接调用 uuid.uuid1() 并转化为字符串返回
        return str(uuid.uuid1())

class GenerateEncryptionUtil:
    """Encryption utility class."""

    def gen_hmac_shax(self, secretKey, msg, digestmod="HmacSHA1"):
        """
        使用 HMAC 加密消息，模拟PHP中的 hash_hmac 函数。

        :param secretKey: 密钥，必须是字符串类型。
        :param msg: 待加密的信息，必须是字符串类型。
        :param digestmod: 指定哈希算法的类型，可以是 'HmacSHA256' 或 'HmacSHA1'。

        :return: 使用 base64 编码的 HMAC 签名。

        注意：
        - PHP 和 Python 在输出时可能有细微差别，所以需要考虑输出格式的一致性。
        - 当使用 hmac.digest() 方法时，PHP 中应该使用原始二进制数据输出。
        - 当使用 hmac.hexdigest() 方法时，可以不传递 raw_output 参数给 PHP 的 hash_hmac 函数。
        """
        # 根据 digestmod 选择对应的哈希函数
        if digestmod == "HmacSHA256":
            hasher = hashlib.sha256
        elif digestmod == "HmacSHA1":
            hasher = hashlib.sha1
        else:
            raise ValueError("Unsupported digest mode provided.")

        # 加密后得到原始二进制数据
        data_bytes = hmac.new(secretKey.encode('utf-8'), msg=msg.encode('utf-8'), digestmod=hasher).digest()
        # 使用 base64 编码 HMAC 签名
        signature = base64.b64encode(data_bytes)

        # 编码消息内容
        if not isinstance(msg, bytes):
            msg = msg.encode('utf-8')

        # 避免时序攻击（如果有 compare_digest 方法则使用它）
        if hasattr(hmac, 'compare_digest'):
            expected = hmac.new(secretKey.encode('utf-8'), msg=msg, digestmod=hasher).digest()
            # 使用 constant-time 比较签名是否匹配
            if not hmac.compare_digest(data_bytes, expected):
                raise ValueError("HMAC signature does not match")
        else:
            # 使用 hashlib 新建算法实例进行比较
            hash_algorithm = hashlib.new(hasher.name, key=secretKey.encode('utf-8'), msg=msg)
            if not hash_algorithm.hexdigest() == data_bytes.hex():
                raise ValueError("HMAC signature does not match")

        return signature
