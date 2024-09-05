#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2022-07-28 16:17:47
modify by: 2024-03-18 19:34:04

功能描述：封装 ipaddress 库的函数，进行 IP 地址相关操作。
"""
import socket
import ipaddress


class IpaddressUtils:
    """IP 地址实用工具类，提供验证 IP 地址和网络地址有效性的方法。"""
    def __init__(self) -> None:
        pass

    def _ip_network(self, network):
        '''
        验证网络地址是否合法；如果输入值异常，返回None
        '''
        try:
            return ipaddress.ip_network(network)
        except ValueError as e:
            print(f"Invalid network address '{network}': {e}")
            return None

    def _ip_address(self, address):
        '''
        验证IP是否合法；如果输入值异常，返回None
        '''
        try:
            return ipaddress.ip_address(address)
        except ValueError as e:
            print(f"Invalid IP address '{address}': {e}")
            return None

    def check_ipaddress(self, address:str, network_list:list = None) -> bool:
        """
        验证给定的 IP 地址是否属于指定的网络地址列表中的任意一个。

        :param address: 要验证的 IP 地址字符串
        :param network_list: 网络地址字符串列表
        :return: 如果 IP 地址属于网络列表中的任意网络，返回 True，否则返回 False
        """
        valid_address = self._ip_address(address)
        if not valid_address or not network_list:
            return False
        
        for network_str in network_list:
            network = self._ip_network(network_str)
            if network and valid_address in network:
                return True
        return False

    def get_internal_ip(self):
        """
        获取本地内网IP地址。

        :return: 本地内网IP地址字符串。
        """
        # 监听一个无效的地址，0.0.0.0代表本地任意IPv4地址
        # 这个方法不会创建网络活动
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # 不需要实际连接到外部服务器
                s.connect(('10.255.255.255', 1))
                internal_ip = s.getsockname()[0]
            return internal_ip
        except Exception as e:
            print(f"无法获取内网IP地址: {e}")
            return None
