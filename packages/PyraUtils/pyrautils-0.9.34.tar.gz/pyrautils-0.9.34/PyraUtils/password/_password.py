
import secrets
import string


class PasswordMaker:
    """
    密码生成器
    用于生成随机密码。
    """
    @staticmethod
    def make_random_password(length:int=10, allowed_chars:str=None) -> str:
        """
        生成一个随机密码。

        :param length: 指定生成密码的长度，默认为10。
        :param allowed_chars: 指定可用于构造密码的字符集合。如果未指定，则使用一个默认的字符集合。
        :return: 一个随机生成的密码字符串。
        """
         # 如果没有指定允许的字符集合，则使用默认的安全字符集。
        if not allowed_chars:
            allowed_chars = string.ascii_letters + string.digits + string.punctuation
            
        # 生成随机密码直到达到需要的长度。
        return ''.join(secrets.choice(allowed_chars) for _ in range(length))


class PasswordStrength:
    """
    密码强度检查器

    弱口令字典地址: 
    https://github.com/wwl012345/PasswordDic
    https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
    """
    def __init__(self, words_path=None):
        """
        初始化 PasswordStrength 对象。

        :param words_path: 弱口令字典文件路径。如果不提供，则需要后续手动设置 word_set 属性。
        :raises FileNotFoundError: 如果指定的文件不存在。
        """

        self.word_set = set()
        if words_path:
            try:
                with open(words_path) as f:
                    # 从给定文件中读取并存储弱密码库。
                    self.word_set.update(line.strip() for line in f)
            except FileNotFoundError:
                raise FileNotFoundError("弱口令字典不存在，请下载以下字典："
                                        "https://github.com/wwl012345/PasswordDic"
                                        "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")

    def is_weak_password(self, pw_str) -> bool:
        """
        根据预定义的弱口令字典检测密码是否弱。

        :param pw_str: 要检测的密码字符串。
        :return: 如果密码被认为是弱密码返回 True，否则返回 False。
        """
        return any(pw_str.lower() == word.lower() for word in self.word_set)

    def password_strength(self, pw_str):
        """
        评估密码的复杂度，并根据结果分类。

        :param pw_str: 要评估的密码字符串。
        :return: 密码的强度等级（'WEAK', 'MEDIUM', 'STRONG'）。
        """
        if len(pw_str) < 8 or self.is_weak_password(pw_str):
            # 如果密码少于8个字符或者在弱密码库中出现，返回WEAK
            return 'WEAK'
        
        char_classes = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation
        ]
        strength_score = sum(bool(set(char_class) & set(pw_str)) for char_class in char_classes)
        # 计算密码中包含的不同字符类别数量
        if len(pw_str) >= 12 and strength_score == 4:
            # 如果密码长度大于等于12并且包含所有四种字符类别，返回STRONG
            return 'STRONG'
        else:
            # 其余情况视为MEDIUM
            return 'MEDIUM'
