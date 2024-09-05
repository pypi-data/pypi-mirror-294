# -*- coding: utf-8 -*-
"""
Created on 2022-07-05 18:03:02
Modified on 2024-07-29 11:05:32
Purpose: 提供JSON Web Token认证功能
"""

import datetime
from typing import Tuple, Dict, Any, Callable
from authlib.jose import jwt, JoseError


# 设置JWT选项配置
jwt_options = {
    'verify_signature': True,
    'verify_exp': True,     # 验证令牌是否过期
    'verify_nbf': False,
    'verify_iat': True,     # 验证令牌发布时间
    'verify_aud': True,     # 验证受众字段
    'verify_iss': False     # 验证发行者字段
}

class JWTDecorator:
    '''
    JSON Web Token装饰器类。

    参考链接: https://github.com/paulorodriguesxv/tornado-json-web-token-jwt/blob/master/auth.py
    '''

    def __init__(self, auth_method='bearer', secret_key='my_secret_key', audience=None, 
                 algorithms=['HS256']):
        """
        初始化JWTDecorator类。

        :param auth_method: 验证方法，默认为 bearer
        :param secret_key: 密钥，如果没有指定，则使用默认密钥 "my_secret_key"
        :param audience: 颁发令牌的受众
        :param algorithms: 使用的算法，默认为 HS256
        """
        self.secret_key = secret_key
        self.audience = audience
        self.auth_method = auth_method
        self.algorithms = algorithms

    def is_valid_header(self, parts):
        """
        检查头部是否有效。

        :param parts: 授权头部信息分割后的列表
        :return: 布尔值，头部信息有效返回True，否则返回False
        """
        return parts and len(parts) == 2 and parts[0].lower() == self.auth_method

    def return_auth_error(self, handler, message: Dict[str, str]):
        """
        返回授权错误。

        :param handler: Tornado的RequestHandler对象
        :param message: 错误消息字典
        """
        handler.set_status(401)
        handler.set_header('WWW-Authenticate', f'{self.auth_method.capitalize()} realm="Restricted"')
        handler.finish(message)


    def require_auth(self, auth_header):
        """
        在执行handler前验证请求是否经过授权。

        :param auth_header: RequestHandler对象
        :param kwargs: 其他关键字参数
        """
        auth = auth_header.request.headers.get('Authorization', None)
        if not auth:
            self.return_auth_error(auth_header, {'message': '参数错误!', 'reason': '缺少Authorization'})
            return False

        parts = auth.split()
        if not self.is_valid_header(parts):
            self.return_auth_error(auth_header, {'message': '验证错误', 'reason': '无效的Authorization头'})
            return False

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                claims_options=jwt_options,
                claims_params={'aud': self.audience},
                algorithms=self.algorithms,
            )
        except JoseError as err:
            self.return_auth_error(auth_header, {'message': 'Token无效', 'reason': str(err)})
            return False
        
        # 将解码后的payload添加到请求的属性中
        setattr(auth_header, '_jwt_payload', payload)
        return True

    def jwtauth(self, func: Callable = None, framework: str = 'flask'):
        if framework == 'flask':
            return self._flask_jwtauth(func)
        elif framework == 'tornado':
            return self._tornado_jwtauth(func)
        else:
            raise ValueError("Unsupported framework")

    def _flask_jwtauth(self, func: Callable):
        """
        Flask JWT 认证装饰器。

        :param func: Flask的路由处理函数
        :return: 装饰后的函数
        """
        def wrapper(*args, **kwargs):
            from flask import request     # 延迟导入 Flask 的 request 对象
            if not self.require_auth(request):
                return {'message': 'Unauthorized'}, 401
            return func(*args, **kwargs)
        return wrapper

    def _tornado_jwtauth(self, handler_class: Any):
        """
        Tornado JWT 认证装饰器。

        :param handler_class: Tornado的RequestHandler类
        :return: 装饰后的类
        """
        execute_orig = handler_class._execute

        def _execute(self, transforms, *args, **kwargs):
            if not self.require_auth(self):
                return {'message': 'Unauthorized'}, 401      # 认证失败时直接返回，不再执行后面的操作
            return execute_orig(self, transforms, *args, **kwargs)

        handler_class._execute = _execute
        return handler_class


class JWT:
    def __init__(self, secret_key: str = 'my_secret_key'):
        """
        初始化JWT类。

        :param secret_key: 密钥，如果没有指定，则使用默认密钥 "my_secret_key"
        """
        self.secret_key = secret_key

    def jwt_encode(self, payload: Dict[str, Any], algorithm: str = 'HS256', exp_seconds: int = 3600) -> Dict[str, str]:
        """
        生成JWT token字符串。

        :param payload: 要编码的数据
        :param algorithm: 编码算法，默认为 HS256
        :param exp_seconds: token的过期时间（秒），默认为1小时
        :return: 包含 JWT token 的字典对象
        """

        # jwt库会将这些datetime对象转化成相应的Unix时间戳。
        now = datetime.datetime.now(datetime.timezone.utc)
        payload.update({
            'exp': now + datetime.timedelta(seconds=exp_seconds),
            'iat': now,
        })

        header = {'alg': algorithm}
        encoded = jwt.encode(
            header,
            payload,
            self.secret_key
        )
        return {'token': encoded.decode() if isinstance(encoded, bytes) else encoded}

    def jwt_decode(self, jwt_token: str, audience: str = None, algorithms: list = ['HS256']) -> Tuple[bool, Dict[str, Any]]:
        """
        解码 JWT token。

        :param jwt_token: 要解码的 token
        :param audience: 颁发令牌的受众
        :param algorithms: 解码算法，默认为 HS256
        :return: tuple，第一个元素指示 token 是否有效，第二个元素是包含结果的字典对象
        """
        try:
            decoded = jwt.decode(
                jwt_token,
                self.secret_key,
                claims_options=jwt_options,
                claims_params={'aud': audience},
                algorithms=algorithms
            )
            # 检查令牌是否过期
            exp_timestamp = decoded.get('exp')
            now_timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
            if now_timestamp > exp_timestamp:
                raise JoseError('Token expired')

            return True, {'message': 'Token is valid!', 'data': decoded}
        except JoseError as err:
            return False, {'message': 'Token is invalid!', 'reason': str(err)}
