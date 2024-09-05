#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cerberus import Validator

class CerberusUtil:
    def __init__(self):
        self.validator = Validator()

    def validate(self, document, schema):
        """
        使用 Cerberus 验证器来验证给定的文档是否符合给定的模式。

        参数：
        - document: 要验证的文档。例如，{"name": "John", "age": 30}
        - schema: 包含验证规则的模式。例如，{"name": {"type": "string"}, "age": {"type": "integer"}}

        返回值：
        - 如果文档有效，则返回 True；否则返回 False。
        
        """
        return self.validator.validate(document, schema)

    def errors(self):
        """
        获取最近一次验证操作的错误字典。

        返回值：
        - 包含验证错误信息的字典。
        """
        return self.validator.errors
