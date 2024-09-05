# -*- coding: utf-8 -*-

import hashlib

'''
区别：
1. hashlib 中的md5 是没有key的，最多是加salt； 而 hmac 是必须加key和指定具体的算法
2. 使用hmac算法比标准hash算法更安全，因为针对相同的password，不同的key会产生不同的hash。
'''

class HashlibUtil:
    def sign(self, digestmod:str, data:bytes):
        """
        使用指定的哈希算法计算给定数据的数字签名。

        :param digestmod: 哈希算法的名称，这个名称可以是 hashlib 支持的任何标准哈希算法，
                        也可以是 OpenSSL 库提供的其他算法。例如 'sha256' 或 'md5'。
                        推荐使用构造器函数（如 hashlib.sha256()）来创建哈希对象，
                        因为它比使用 new() 方法更直接且效率更高。

            常用的算法 - 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'
                                    'blake2b', 'blake2s', 'shake_128', 'shake_256'
                                    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'
        :param data: 要被哈希处理的原始数据，必须是字节类型。

        :return: 返回一个字节字符串，该字符串包含了数据的哈希摘要（数字签名）。

        :raises TypeError: 如果 'digestmod' 参数不是字符串类型，则抛出类型错误。

        注意：应当总是优先使用安全性较高的哈希算法。例如 SHA-2 系列（如 'sha256'）或 SHA-3 系列算法，
            不建议使用已经不再安全的 'md5' 或 'sha1' 算法进行数据签名。
        """
        # 验证输入参数类型
        if not isinstance(digestmod, str):
            raise TypeError("Algorithm name must be a string")

        # 创建一个新的哈希对象，使用指定的算法
        h = hashlib.new(digestmod)

        # 更新哈希对象的状态以反映给定的数据
        h.update(data)

        # 计算并返回数据的哈希摘要
        return h.digest()

    def sign_derivation(self, hash_name:str, password:bytes, salt:bytes, iterations:int=100000, dklen=None):
        """
        使用 PBKDF2 (Password-Based Key Derivation Function 2) 方法根据指定的哈希算法从密码和盐值派生加密密钥。

        :param hash_name: 哈希算法名称，例如 'sha256' 或 'sha512'。
        :param password: 用于生成密钥的密码，必须是字节类型。
        :param salt: 加盐增强密码的安全性，必须是字节类型。
        :param iterations: 指定哈希算法迭代的次数，默认为 100000 次。提高此值可以让密码更安全但会增加计算时间。
        :param dklen: 期望得到密钥的长度（以字节为单位）。如果不设置，则使用所选哈希算法的默认长度。

        :return: 返回以十六进制表示的派生密钥字符串。

        :raises TypeError: 如果 'password' 或 'salt' 不是字节类型，则抛出类型错误。
        :raises ValueError: 如果密码长度超过 1024 字节，则抛出值错误，因为密码应限制为合理大小。

        注意：密钥长度（dklen）如果未指定将默认为哈希算法输出的长度。例如对于 SHA-256，默认密钥长度是 256 位（32字节）。
        """
        # 验证输入参数类型
        if not isinstance(password, bytes) or not isinstance(salt, bytes):
            raise TypeError("Password and salt must be bytes")

        # 对密码长度进行限制以防止不合理的大小
        if len(password) > 1024:
            raise ValueError("Password length should be limited to reasonable size")

        # 使用 PBKDF2 算法进行密钥派生
        dk = hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen)
    
        # 返回十六进制编码的派生密钥
        return dk.hex()

    def sign_blake2b(self, data: bytes = b'', digest_size: int = 64, key: bytes = b'', salt: bytes = b'',
                    person: bytes = b'', fanout: int = 1, depth: int = 1, leaf_size: int = 0,
                    node_offset: int = 0, node_depth: int = 0, inner_size: int = 0,
                    last_node: bool = False, usedforsecurity: bool = True):
        '''
        生成一个使用 BLAKE2b 哈希算法的签名。

        :param data: 要哈希的初始数据块，它必须为 bytes-like 对象。 它只能作为位置参数传入。
        :param digest_size: 以字节数表示的输出摘要大小，默认为 64 字节。
        :param key: 用于密钥哈希的密钥（对于 BLAKE2b 最长 64 字节）。
        :param salt: 用于随机哈希的盐值（对于 BLAKE2b 最长 16 字节）。
        :param person: 个性化字符串（对于 BLAKE2b 最长 16 字节）。
        :param fanout: 树模式的扇出参数。默认为 1。
        :param depth: 树模式的最大树深度。默认为 1。
        :param leaf_size: 树模式中叶子节点的字节长度。默认为 0。
        :param node_offset: 树模式中节点的偏移量。默认为 0。
        :param node_depth: 树模式中当前节点的深度。默认为 0。
        :param inner_size: 内部节点输出字节长度。默认为 0。
        :param last_node: 布尔标志，指示这是否是给定层级的最后节点。默认为 False。
        :param usedforsecurity: 布尔标志，指示哈希函数是否用于安全敏感的操作。默认为 True。

        :return: 返回用十六进制表示的摘要字符串，并编码为 utf-8 格式的 bytes 阵列。

        :raises TypeError: 如果 'data', 'key', 'salt', 或 'person' 参数不是 bytes 类型，则抛出类型错误。
        '''
        # 验证输入参数类型
        if not isinstance(data, bytes) or not isinstance(key, bytes) or not isinstance(salt, bytes) or not isinstance(person, bytes):
            raise TypeError("data, key, salt and person must be bytes")

        # 初始化 BLAKE2b 哈希对象
        h = hashlib.blake2b(digest_size=digest_size, key=key, salt=salt,person=person,
                            fanout=fanout, depth=depth, leaf_size=leaf_size, node_offset=node_offset,
                            node_depth=node_depth, inner_size=inner_size,
                            last_node=last_node, usedforsecurity=usedforsecurity)
        # 更新哈希对象与给定的数据
        h.update(data)
        # 返回以十六进制表示且编码为 utf-8 的哈希摘要
        return h.hexdigest().encode('utf-8')
