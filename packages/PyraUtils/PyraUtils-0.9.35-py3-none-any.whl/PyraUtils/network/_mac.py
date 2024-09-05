#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2024-03-06
modify by: 2024-03-06

功能：MAC地址相关的基础方法
"""

import re

class MacHandler:
    def standardize_mac_address(self, mac):
        # 移除所有非十六进制字符进行清洗
        sanitized_mac = re.sub(r'[^0-9A-Fa-f]', '', mac)

        # 将MAC地址格式化为冒号分隔的格式
        colon_separated_mac = ':'.join(sanitized_mac[i:i+2] for i in range(0, 12, 2))
        
        # 转换为大写
        return colon_separated_mac.upper()

    def is_valid_mac_address(self, mac):
        # 正则表达式匹配典型的MAC地址格式
        #
        # 此函数的作用是确认输入的MAC地址是否符合两种常见的表示方式：
        # 01:23:45:67:89:ab - 使用冒号(:)分隔的形式。
        # 01-23-45-67-89-ab - 使用连字符(-)分隔的形式。

        # 删除MAC地址字符串前后的空格
        mac = mac.strip()

        pattern = re.compile(r"""
            ^([0-9A-Fa-f]{2}[:-]){5}    # 前五组十六进制数字加分隔符
            ([0-9A-Fa-f]{2})$          # 最后一组十六进制数字（无后续分隔符）
            """, re.VERBOSE)
        
        # 使用正则表达式检查MAC地址是否有效
        if pattern.match(mac):
            return True
        else:
            return False