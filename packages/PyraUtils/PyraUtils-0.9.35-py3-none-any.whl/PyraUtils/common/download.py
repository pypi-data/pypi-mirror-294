#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2018-2-23 14:15:57
modify by: 2023-05-13 15:05:05

功能：各种常用的方法函数的封装。
"""

import os
import urllib3
from contextlib import closing
import requests
import httpx
import rich.progress
from tqdm import tqdm

from loguru import logger

class DownloadUtil:
    """DownloadUtil, 工具类
    Attributes:
    """

    @staticmethod
    def dl_01(url:str, dl_path:str, timeout:int = 10, **kwargs) -> bool:
        '''
        使用requests实现下载
        :param url: 下载文件的URL地址
        :param dl_path: 下载文件保存的路径
        :param timeout: 超时时间，默认为10秒
        :param kwargs: 其他可选参数传递给requests.get()
        :return: 下载是否成功的标识
        '''

        try:
            # 检查保存文件的目录是否存在，如果不存在则创建
            os.makedirs(os.path.dirname(dl_path), exist_ok=True)
            resp = requests.get(url, timeout=timeout, **kwargs,)
                # 在有异常的情况下抛出异常
            resp.raise_for_status()
            with open(dl_path, "wb") as f:
                f.write(resp.content)
        except (requests.RequestException, IOError) as err:
            logger.error(f"Error occurred while downloading {url}: {err}")
            return False # 返回下载失败标识

    @staticmethod
    def dl_02(url:str, dl_path:str, timeout: float = 10, **kwargs) -> None:
        '''
        使用urllib3实现下载
        :param url: 下载文件的URL地址
        :param dl_path: 下载文件保存的路径
        :param timeout: 超时时间（秒），默认为None，即无限等待
        :param kwargs: 其他可选参数传递给http.request()
        :return: None

        dl_02('https://example.com/file.zip', 'path/to/save/file.zip')
        '''
        # 创建连接池管理器
        http = urllib3.PoolManager(timeout=timeout)
         # 发送请求并获取响应
        response = http.request('GET', url, **kwargs)
        # 检查保存文件的目录是否存在，如果不存在则创建
        os.makedirs(os.path.dirname(dl_path), exist_ok=True)
        # 读取响应内容并保存到文件中
        with open(dl_path, 'wb') as f:
            f.write(response.data)

    @staticmethod
    def dl_03(url:str, dl_path:str, **kwargs) -> str:
        '''
        使用requests实现下载,同时增加对特定情况下的判断
        '''
        with closing(requests.get(url, stream=True, **kwargs)) as resp:
            # 判断下载链接是否异常
            resp.raise_for_status()

            # 判断下载链接是否异常
            resp_code = resp.status_code
            if 299 < resp_code or resp_code < 200:
                logger.warning('returnCode %s %s' % (resp_code, url))

            # 判断下载文件是否为0
            content_length = int(resp.headers.get('content-length', '0'))
            if content_length == 0:
                return f'size0 {url}'

            try:
                with open(dl_path, 'wb') as f:
                    for data in resp.iter_content(1024):
                        f.write(data)
            except requests.exceptions.RequestException as e:
                return f'RequestError {str(e)}'
            except IOError as e:
                return f'SaveError {str(e)}'

            return 'success'

    @staticmethod
    def dl_04(url: str, dl_path: str, chunk_size: int = 1024, **kwargs) -> None:
        '''
        使用requests实现下载,大文件专用
        '''

        # 判断是否支持断点续传
        headers = kwargs.get('headers', {})
        if 'Range' not in headers and os.path.exists(dl_path):
            headers['Range'] = f'bytes={os.path.getsize(dl_path)}-'

        with requests.get(url, stream=True, headers=headers, **kwargs) as resp:
            resp.raise_for_status()

            with open(dl_path, 'ab') as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    f.write(chunk)

class DownloadProgressUtil:
    """DownloadProgressUtil, 工具类

    Attributes:

    """
    def __init__(self, chunk_size = 1024) -> None:
        self.chunk_size = chunk_size

    def dl_01(self, url, dl_path, **kwargs):
        '''
        使用tqdm库来显示下载进度条
        '''
        # 创建文件夹（如果不存在）并打开文件以写入下载的数据
        if not os.path.exists(os.path.dirname(dl_path)):
            os.makedirs(os.path.dirname(dl_path), exist_ok=True)

        # 发送GET请求并获得响应对象
        with open(dl_path, 'wb') as out_file:
            # 需要把kwargs作为一个字典传递给stream()方法，而不是一个位置参数
            with httpx.stream("GET", url, **kwargs) as resp:
                # 确定文件的总大小（字节数）
                total_length = int(resp.headers.get("Content-Length", 0))

                with tqdm(total=total_length, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                    num_bytes_downloaded = resp.num_bytes_downloaded
                    for chunk in resp.iter_bytes(chunk_size=self.chunk_size):
                        out_file.write(chunk)
                        progress.update(resp.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = resp.num_bytes_downloaded

    def dl_02(self, url, dl_path, **kwargs):
        '''
        使用rich实现进度条
        '''
        with open(dl_path, 'wb') as out_file:
            # 需要把kwargs作为一个字典传递给stream()方法，而不是一个位置参数
            with httpx.stream("GET", url, **kwargs) as resp:
                total_length = int(resp.headers.get("Content-Length", 0))

                with rich.progress.Progress(
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    rich.progress.BarColumn(bar_width=None),
                    rich.progress.DownloadColumn(),
                    rich.progress.TransferSpeedColumn(),
                ) as progress:
                    download_task = progress.add_task("Download", total=total_length)
                    for chunk in resp.iter_bytes(chunk_size=self.chunk_size):
                        out_file.write(chunk)
                        progress.update(download_task, completed=resp.num_bytes_downloaded)

