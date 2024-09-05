'''
通过将可能的明文密码转换为散列值，并与Wireshark捕获的散列值进行比较，从而找到匹配项。
这种方法通常被称为“散列碰撞”或“彩虹表攻击”，它是基于尝试许多不同的可能的密码，直到找到一个其散列值与捕获的散列值相匹配的密码。

下面是一个简化的流程描述：

你有一个Wireshark捕获的加密（散列）的密码，例如MD5、SHA1、SHA256等。
你创建一个包含可能明文密码的列表。
对于列表中的每个明文密码，你使用相同的散列算法生成散列值。
将生成的散列值与Wireshark捕获的散列值进行比较。
如果某个生成的散列值与捕获的散列值相匹配，那么你可以假设相应的明文密码就是原始密码。
这种方法的有效性取决于你的密码列表是否包含了正确的密码。如果列表中没有正确的密码，你将无法找到匹配的散列值。
此外，如果使用了强散列函数和/或额外的安全措施（如盐值），即使你有正确的密码，也可能无法找到匹配的散列值。

'''

import base64
import hashlib

class PasswordHashTester:
    def __init__(self, hash_algorithms=None):
        """
        初始化密码散列测试器类。

        :param hash_algorithms: 一个字典，键为散列算法的名称，值为对应的散列函数。如果为None，则使用默认算法集。
        """
        if hash_algorithms is None:
            self.hash_algorithms = {
                'MD5': hashlib.md5,
                'SHA1': hashlib.sha1,
                'SHA224': hashlib.sha224,
                'SHA256': hashlib.sha256,
                'SHA384': hashlib.sha384,
                'SHA512': hashlib.sha512,
                # 可以添加更多的算法
            }
        else:
            self.hash_algorithms = hash_algorithms

    @staticmethod
    def decode_base64(encoded_str):
        """
        对base64编码的字符串进行解码。

        :param encoded_str: base64编码的字符串。
        :return: 解码后的bytes，如果解码失败则返回None。
        """
        try:
            decoded_bytes = base64.b64decode(encoded_str)
            return decoded_bytes
        except base64.binascii.Error as e:
            print(f"解码错误: {e}")
            return None

    def test_password_hash(self, captured_hash, test_passwords):
        """
        测试一系列明文密码与不同的散列算法是否与已捕获的散列密码匹配。

        :param captured_hash: 散列密码字符串。
        :param test_passwords: 要测试的明文密码列表。
        :return: None
        """
        for password in test_passwords:
            for hash_name, hash_func in self.hash_algorithms.items():
                calculated_hash = hash_func(password.encode()).hexdigest()
                if calculated_hash == captured_hash:
                    return {'algorithm': hash_name, 'password': password}
        return None


# # 使用示例
# if __name__ == "__main__":
#     tester = PasswordHashTester()

#     encoded_pass = "c2FsdF8xMXhsayE1MjAxMDA="
#     captured_passwd = "b3aa4ca75ecb6681f9a543674d8e3c88"
#     test_passwords = ['password123', 'letmein', '123456', 'xlk!520100']

#     decoded_pass = tester.decode_base64(encoded_pass)
#     if decoded_pass is not None:
#         test_passwords.append(decoded_pass.decode())

#     match_info = tester.test_password_hash(captured_passwd, test_passwords)
#     if match_info:
#         print(f"找到匹配项，算法：{match_info['algorithm']}, 密码：{match_info['password']}")
#     else:
#         print("没有找到匹配项。")
