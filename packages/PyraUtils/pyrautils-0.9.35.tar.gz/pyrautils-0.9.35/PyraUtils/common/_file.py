#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2018-2-23 14:15:57
modify by: 2023-05-17 17:46:40

功能：封装常见文件操作的工具类，包括打开大文件、创建目录、复制目录树、获取目录下的文件列表、更改文件所有权、
      批量重命名文件、单个文件重命名以及压缩与解压文件。
"""
import os
from pathlib import Path
import gzip
import lzma
import shutil
import tarfile
import zipfile
import py7zr
import platform

class FileUtils:
    """FileUtils"""
    @staticmethod
    def open_lagre_file(filename:str):
        """
        逐行读取大文件，使用生成器避免一次性加载整个文件到内存中。

        :param filename: 要逐行读取的文件路径
        :type filename: str
        :yield: 文件的每一行内容
        """
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()

    @staticmethod
    def create_folder(str1:str) -> None:
        """
        创建目录，如果目录的上级目录不存在，也会被创建。

        :param str1: 要创建的目录路径
        :type str1: str
        """
        Path(str1).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def copy(src:str, dst:str, ignore=None, dirs_exist_ok=True) -> None:
        """
        递归地复制一个目录树到指定目录。

        :param src: 源目录的路径。
        :param dst: 目标目录的路径，该目录必须不存在。
        :param ignore: 可选参数, 默认为None。忽略复制时的某些文件/目录，使用shutil.ignore_patterns()函数指定。
        :param dirs_exist_ok: 可选参数，默认为True。当目标目录存在时是否抛出异常。
        
        如果目标目录已经存在，并且dirs_exist_ok设置为False，则会抛出OSError异常。
        """

        if ignore:
            # 忽略文件时，可以使用shutil.ignore_patterns()函数来指定要忽略的文件类型或者目录名
            # ignore=shutil.ignore_patterns('*.pyc', 'tmp*')"
            ignore = shutil.ignore_patterns(ignore)

        if not os.path.exists(dst) and os.path.exists(src):
             # 如果目录不存在，则递归复制源目录
             # 目标目录存在时，如果设置了dirs_exist_ok参数为True，则不会抛出异常
            shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=dirs_exist_ok)
        else:
            raise OSError("The target path already exists! After a minute retry ~!")

    @staticmethod
    def get_listfile_01(path:str) -> list:
        """
        使用os.walk()遍历指定目录, 返回目录下所有文件的路径(不包含文件夹).
        
        参数:
        path: str - 指定的目录路径.
        
        返回值:
        list - 包含指定目录下所有文件的路径的列表.
        """
        file_path_list = []
        for root, _, files in os.walk(path):
            file_path_list.extend(os.path.join(root, f) for f in files)

        return file_path_list

    @staticmethod
    def get_listfile_02(path:str) -> list:
        """
        使用递归遍历指定目录, 返回目录下所有文件的路径(不包含文件夹).
        
        参数:
        path: str - 指定的目录路径.
        
        返回值:
        list - 包含指定目录下所有文件的路径的列表.

        os.scandir()可能相较os.walk()性能更高，尤其在列出大量目录内容时。
        """
        file_path_list = []
        def scan_dir(dir):
            for entry  in os.scandir(dir):
                if entry.is_file():
                    file_path_list.append(entry.path)
                # 如果entry是文件夹，则递归调用scan_dir()来扫描其内部
                elif entry.is_dir():
                    scan_dir(entry.path)

        scan_dir(path)
        return file_path_list

    @staticmethod
    def get_listfile_03(path: str, include_files: bool = True, include_dirs: bool = False) -> list:
        """获取指定目录下的所有文件和文件夹列表.

        :param path: 目标文件夹路径.
        :type path: str
        :param include_files: 是否包含文件. (默认值为True.)
        :type include_files: bool
        :param include_dirs: 是否包含子文件夹. (默认值为False.)
        :type include_dirs: bool
        :return: 返回path下的文件或文件夹列表list.
        :rtype: list
        """
        if not os.path.exists(path):
            raise OSError(f"路径 {path} 不存在！")

        file_list = []
        dir_list = []

        for root, dirs, files in os.walk(path, topdown=False):
            if include_files:
                file_list.extend([os.path.join(root, f) for f in files])
            if include_dirs:
                dir_list.extend([os.path.join(root, d) for d in dirs])

        if include_dirs is False and include_files is True:
            return file_list
        elif include_dirs is True and include_files is False:
            return dir_list
        elif include_dirs is True and include_files is True:
            return [*file_list, *dir_list]
        else:
            raise ValueError("参数include_files/include_dirs无效！")

    @staticmethod
    def change_owner(src, uid, gid, loop=False):
        '''
        更改指定文件或目录的所有者（UID）和所属组（GID）

        src：要更改所有权的文件或目录路径；
        uid：新的所有者用户 ID；
        gid：新的所属组 ID；
        loop：bool 类型，可选参数，默认值为 False。
        如果为 True，则在更改目录所有权时也会递归处理其中的所有子文件和子目录。需要注意的是，在递归过程中，代码还会忽略符号链接，并跳过它们（因为在某些情况下，更改符号链接的所有权可能会导致不可预期的后果）。

        # 示例用法
        change_owner('/path/to/dir', 1000, 1000, loop=True)
        '''
        if platform.system().lower() == 'windows':
            raise OSError('Windows 系统无法设置文件或目录的所有者')
        
        if os.path.isfile(src):
            os.chown(src, uid, gid)
        elif os.path.isdir(src) and loop:
            for dirpath, dirnames, filenames in os.walk(src):
                for dirname in dirnames:
                    filepath = os.path.join(dirpath, dirname)
                    if os.path.islink(filepath):  # 如果是符号链接，则跳过
                        continue
                    os.chown(filepath, uid, gid)
                
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.islink(filepath):  # 如果是符号链接，则跳过
                        continue
                    os.chown(filepath, uid, gid)
                    
                    # 如果是目录则递归调用
                    if os.path.isdir(filepath):
                        FileUtils.change_owner(filepath, uid, gid, loop=True)

    @staticmethod
    def rename_files(file_lists:list, file_prefix: str = "", file_suffix: int = 1) -> None:
        """批量重命名文件

        :param file_lists: 要重命名的文件列表，即包含多个文件路径的字符串列表
        :param file_prefix: 新文件名的前缀，字符串类型
        :param file_suffix: 新文件名的后缀，正整数类型
        :return: None

        file_list = ["file1.txt", "file2.txt", "file3.txt"]
        MyClass.rename_files(file_list, "new_", 10)
        """
        if not isinstance(file_suffix, int) or file_suffix <= 0:
            raise ValueError("file_suffix must be a positive integer")

        backup_names = []

        try:
            for f in file_lists:
                backup_names.append(os.path.basename(f))
                _, file_ext = os.path.splitext(f)
                new_name = f"{file_prefix}{file_suffix + len(backup_names) - 1:03d}{file_ext}"
                os.rename(f, new_name)
        except Exception as e:
            print(f"Failed to rename {f}, error: {e}")
            # 回滚重命名操作
            for i, f in enumerate(file_lists):
                backup_name = backup_names[i]
                os.rename(f"{file_prefix}{i+file_suffix:03d}{os.path.splitext(f)[1]}", backup_name)


    def rename_file(old_path: str, new_path: str) -> None:
        """
        重命名单个文件。

        :param old_path: 原文件路径。
        :param new_path: 新文件路径。
        
        如果新路径的文件已存在，将抛出FileExistsError异常。
        """
        try:
            if Path(new_path).exists():
                raise FileExistsError(f"{new_path} already exists.")
            Path(old_path).rename(new_path)
        except OSError as e:
            print(f"Error renaming {old_path} to {new_path}: {e}")

#####
####  压缩包方法       
#####


def get_compress_types():
    """
    返回支持的压缩类型与相应打开文件的函数和模式。

    :return: 压缩类型与函数、模式的映射字典。
    """
    return {
        "gz": (gzip.open, 'wb'),  # .gz 文件使用 gzip.open 打开，并以写入（w）二进制（b）模式
        "bz2": (gzip.open, 'wb'),  # .bz2 文件也使用 gzip.open 打开，并以写入（w）二进制（b）模式
        "xz": (lzma.open, 'wb'),  # .xz 文件使用 lzma.open 打开，并以写入（w）二进制（b）模式
        "zip": (zipfile.ZipFile, 'w'),  # .zip 文件使用 ZipFile 打开，并以写入（w）模式
        "7z": (py7zr.SevenZipFile, 'w')  # .7z 文件使用 SevenZipFile 打开，并以写入（w）模式
    }

def get_compression_formats():
    """
    返回支持的压缩格式对应的tarfile模式。

    :return: 压缩类型与tarfile模式的映射字典。
    """
    return {
        "gz": "r:gz",  # .gz 文件采用 "r:gz" 解压格式
        "tgz": "r:gz",  # .tgz 文件也采用 "r:gz" 解压格式
        "bz2": "r:bz2",  # .bz2 文件采用 "r:bz2" 解压格式
        "xz": "r:xz",  # .xz 文件采用 "r:xz" 解压格式
        "zip": None,  # .zip 文件不需要指定解压格式
        "7z": None  # .7z 文件不需要指定解压格式
    }

class ZipFilesUtils:
    @staticmethod
    def compress_file(source_path, target_path, compress_type="gz"):
        """
        将指定文件进行压缩。

        :param source_path: 要压缩的文件路径。
        :param target_path: 压缩文件保存路径。
        :param compress_type: 压缩类型。
        
        如果压缩类型不受支持，将抛出ValueError异常。
        """
        compress_types = get_compress_types()
        compress_func, mode = compress_types.get(compress_type, (None, None))
        
        if compress_func is None:
            raise ValueError("不支持的压缩类型。")
            
        with open(source_path, 'rb') as f_in, compress_func(target_path, mode) as f_out:
            if compress_type == "zip":
                f_out.write(f_in.read())
            else:
                shutil.copyfileobj(f_in, f_out)

    @staticmethod
    def extract_tar_compress_file(file_path, extract_path, compress_type="gz"):
        """
        解压缩文件到指定目录。

        :param file_path: 压缩文件路径。
        :param extract_path: 解压缩目标目录。
        :param compress_type: 压缩文件类型。
        
        如果压缩类型不受支持，将抛出ValueError异常。
        """
        compression_formats = get_compression_formats()
        compression_format = compression_formats.get(compress_type)
        
        if compression_format is None:
            if compress_type == "zip":
                with zipfile.ZipFile(file_path) as zfile:
                    zfile.extractall(extract_path)  # 对于 zip 文件，使用 extractall() 方法进行解压
            elif compress_type == "7z":
                with py7zr.SevenZipFile(file_path, mode='r') as sfile:
                    sfile.extractall(path=extract_path)  # 对于 7z 文件，使用 extractall() 方法进行解压
            else:
                raise ValueError("不支持的压缩类型。")
        else:
            with tarfile.open(file_path, compression_format) as tar:
                def safe_member_filter(member):
                    # 使用 `isreg` 来检查是否是常规文件，如果不是常规文件则返回 None
                    return member if member.isreg() else None
                
                # 使用 `filter` 参数来确保安全提取
                tar.extractall(path=extract_path, filter=safe_member_filter)