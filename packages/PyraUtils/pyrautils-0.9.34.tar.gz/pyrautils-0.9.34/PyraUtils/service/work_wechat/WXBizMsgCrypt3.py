#!/usr/bin/env python
# -*- encoding:utf-8 -*-

""" 对企业微信发送给企业后台的消息加解密示例代码.
@copyright: Copyright (c) 1998-2014 Tencent Inc.

"""
# ------------------------------------------------------------------------
import base64
import random
import hashlib
import time
import struct
import socket

from Crypto.Cipher import AES
from defusedxml import ElementTree as DefusedET
import loguru

"""
关于Crypto.Cipher模块，ImportError: No module named 'Crypto'解决方案, 下载pycryptodome。
"""

# Description:定义错误码含义 
# https://developer.work.weixin.qq.com/document/path/90313
#########################################################################
WXBizMsgCrypt_OK = 0
WXBizMsgCrypt_ValidateSignature_Error = -40001
WXBizMsgCrypt_ParseXml_Error = -40002
WXBizMsgCrypt_ComputeSignature_Error = -40003
WXBizMsgCrypt_IllegalAesKey = -40004
WXBizMsgCrypt_ValidateCorpid_Error = -40005
WXBizMsgCrypt_EncryptAES_Error = -40006
WXBizMsgCrypt_DecryptAES_Error = -40007
WXBizMsgCrypt_IllegalBuffer = -40008
WXBizMsgCrypt_EncodeBase64_Error = -40009
WXBizMsgCrypt_DecodeBase64_Error = -40010
WXBizMsgCrypt_GenReturnXml_Error = -40011
#########################################################################

logger = loguru.logger.bind(name="WXBizMsgCrypt3")

class FormatException(Exception):
    pass


def throw_exception(message, exception_class=FormatException):
    """my define raise exception function"""
    raise exception_class(message)


class SHA1:
    """计算企业微信的消息签名接口"""

    def getSHA1(self, token, timestamp, nonce, encrypt):
        """用SHA1算法生成安全签名
        
        @param token:  票据
        @param timestamp: 时间戳
        @param encrypt: 密文
        @param nonce: 随机字符串
        @return: 安全签名

        文档: https://developers.weixin.qq.com/miniprogram/dev/framework/server-ability/message-push.html
        """
        try:
            sortlist = [token, timestamp, nonce, encrypt]
            sortlist.sort()
            sha = hashlib.sha1()
            sha.update("".join(sortlist).encode())
            return WXBizMsgCrypt_OK, sha.hexdigest()
        except Exception as e:
            logger.error(e)
            return (WXBizMsgCrypt_ComputeSignature_Error, None)


class XMLParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    def extract(self, xmltext):
        """提取出xml数据包中的加密消息
        @param xmltext: 待提取的xml字符串
        @return: 提取出的加密消息字符串
        """
        try:
            xml_tree = DefusedET.fromstring(xmltext)
            encrypt = xml_tree.find("Encrypt").text
            return (WXBizMsgCrypt_OK, encrypt)
        except Exception as e:
            logger.error("extract fail, xmltext: %s", xmltext)
            return WXBizMsgCrypt_ParseXml_Error, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """生成xml消息"""
        AES_TEXT_RESPONSE_TEMPLATE = f"""<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""
        return AES_TEXT_RESPONSE_TEMPLATE

class PKCS7Encoder():
    """提供基于PKCS7算法的加解密接口"""
    block_size = 32

    def encode(self, text):
        """
        对需要加密的明文进行填充补位

        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)

        # return text + (pad * amount_to_pad).encode()
        return text + pad.encode() * amount_to_pad

    def decode(self, decrypted):
        """
        删除解密后明文的补位字符

        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])   # 获取最后一个字符的ASCII值，即填充长度
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """提供接收和推送给企业微信消息的加解密接口"""

    def __init__(self, key):
        # self.key = base64.b64decode(key+"=")
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text, receiveid):
        """
        对明文进行加密

        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        try:
            # 编码原始文本
            encoded_text = text.encode()

            # 添加随机字符串和长度信息
            random_prefix = self.get_random_str()
            length_info = struct.pack("I", socket.htonl(len(encoded_text)))
            prepared_text = random_prefix + length_info + encoded_text + receiveid.encode()

            # 使用自定义的填充方式对明文进行补位填充
            pkcs7 = PKCS7Encoder()
            padded_text = pkcs7.encode(prepared_text)

            # 加密
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            ciphertext = cryptor.encrypt(padded_text)

            # 使用BASE64对加密后的字符串进行编码
            encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')

            return (WXBizMsgCrypt_OK, encoded_ciphertext)
        except Exception as e:
            logger.error(e)
            return (WXBizMsgCrypt_EncryptAES_Error, None)

    def decrypt(self, text, receiveid):
        """
        对解密后的明文进行补位删除

        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as e:
            logger.error(e)
            return (WXBizMsgCrypt_DecryptAES_Error, None)

        try:
            pad = plain_text[-1]
            # 去掉补位字符串
            # pkcs7 = PKCS7Encoder()
            # plain_text = pkcs7.encode(plain_text)
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])
            xml_content = content[4: xml_len + 4]
            from_receiveid = content[xml_len + 4:]
        except Exception as e:
            logger.error(e)
            return (WXBizMsgCrypt_IllegalBuffer, None)

        if from_receiveid.decode('utf8') != receiveid:
            return WXBizMsgCrypt_ValidateCorpid_Error, None
        return (0, xml_content)

    def get_random_str(self):
        """
        随机生成16位字符串

        @return: 16位字符串
        """
        # return str(random.randint(1000000000000000, 9999999999999999)).encode()
        return random.getrandbits(128).to_bytes(16, 'big')


class WXBizMsgCrypt(object):
    # 构造函数
    def __init__(self, sToken, sEncodingAESKey, sReceiveId):
        try:
            self.key = base64.b64decode(sEncodingAESKey + "=")
            assert len(self.key) == 32
        except:
            throw_exception("[error]: EncodingAESKey unvalid !", FormatException)
            # return WXBizMsgCrypt_IllegalAesKey,None
        self.m_sToken = sToken
        self.m_sReceiveId = sReceiveId

    def VerifyURL(self, sMsgSignature, sTimeStamp, sNonce, sEchoStr):
        '''
        验证URL
        :param sMsgSignature: 签名串，对应URL参数的msg_signature
        :param sTimeStamp: 时间戳，对应URL参数的timestamp
        :param sNonce: 随机串，对应URL参数的nonce
        :param sEchoStr: 随机串，对应URL参数的echostr
        :param sReplyEchoStr: 解密之后的echostr，当return返回0时有效
        :return：成功0，失败返回对应的错误码
        '''
        sha1 = SHA1()
        ret, signature = sha1.getSHA1(self.m_sToken, sTimeStamp, sNonce, sEchoStr)
        if ret != 0:
            logger.error(f'error sha1: {ret}')
            return ret, None

        if not signature == sMsgSignature:
            logger.error(f'error signature: {signature}')
            return WXBizMsgCrypt_ValidateSignature_Error, None

        pc = Prpcrypt(self.key)
        ret, sReplyEchoStr = pc.decrypt(sEchoStr, self.m_sReceiveId)
        return ret, sReplyEchoStr

    def EncryptMsg(self, sReplyMsg, sNonce, timestamp=None):
        '''
        将企业回复用户的消息加密打包

        :param sReplyMsg: 企业号待回复用户的消息，xml格式的字符串
        :param sTimeStamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        :param sNonce: 随机串，可以自己生成，也可以用URL参数的nonce
        :param sEncryptMsg: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串,
        :return：成功0，sEncryptMsg,失败返回对应的错误码None
        '''
        pc = Prpcrypt(self.key)
        ret, encrypt = pc.encrypt(sReplyMsg, self.m_sReceiveId)

        # 在这里检查encrypt是否为None
        if ret != 0 or encrypt is None:
            logger.error(f'error encrypt: {encrypt}')
            return ret, None

        # 由于已经确认encrypt非None，可以安全地调用.decode()
        encrypt = encrypt.decode('utf8')

        if timestamp is None:
            timestamp = str(int(time.time()))

        # 生成安全签名
        sha1 = SHA1()
        ret, signature = sha1.getSHA1(self.m_sToken, timestamp, sNonce, encrypt)
        if ret != 0:
            logger.error(f'error signature: {signature}')
            return ret, None

        xmlParse = XMLParse()
        return ret, xmlParse.generate(encrypt, signature, timestamp, sNonce)

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        '''
        检验消息的真实性，并且获取解密后的明文
        :param sMsgSignature: 签名串，对应URL参数的msg_signature
        :param sTimeStamp: 时间戳，对应URL参数的timestamp
        :param sNonce: 随机串，对应URL参数的nonce
        :param sPostData: 密文，对应POST请求的数据
        :param xml_content: 解密后的原文，当return返回0时有效
        :return: 成功0，失败返回对应的错误码
        '''
        # 验证安全签名
        xmlParse = XMLParse()
        ret, encrypt = xmlParse.extract(sPostData)
        if ret != 0:
            logger.error(f'error encrypt: {encrypt}')
            return ret, None

        sha1 = SHA1()
        ret, signature = sha1.getSHA1(self.m_sToken, sTimeStamp, sNonce, encrypt)
        if ret != 0:
            logger.error(f'error sha1: {ret}')
            return ret, None
        if not signature == sMsgSignature:
            logger.error(f'error signature: {signature}')
            return WXBizMsgCrypt_ValidateSignature_Error, None

        pc = Prpcrypt(self.key)
        ret, xml_content = pc.decrypt(encrypt, self.m_sReceiveId)
        return ret, xml_content
