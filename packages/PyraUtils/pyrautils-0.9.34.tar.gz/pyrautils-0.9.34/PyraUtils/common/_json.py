#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created by：2021-12-02 18:02:15
modify by: 2023-05-12 10:02:18

功能：json函数的封装。
"""

import json
from typing import Any, Optional, Dict

class JsonUtils:
    """JsonUtils, 工具类

    支持加载、保存、更新JSON文件以及判断字符串是否为JSON格式等操作。

    Attributes:

        dumps是将dict转化成str格式，loads是将str转化成dict格式。

        dump和load也是类似的功能，只是与文件操作结合起来了。
    """
    @staticmethod
    def load_json(json_path:str) -> Optional[Dict]:
        """加载json文件并返回一个json对象

        参数：
            Optional[Dict]: 成功时返回字典对象；失败时返回None.

        返回值：
            一个json对象

        异常：
            OSError: 如果文件打开失败
            JSONDecodeError: 如果文件内容不是合法的json格式
        """
        try:
            with open(json_path, "r", encoding="utf8")  as frs:
                return json.load(frs)
        except OSError as e:
            raise OSError(f"Failed to open file {json_path}: {e}")
        except json.JSONDecodeError as e:
            # raise json.JSONDecodeError(f"Failed to decode JSON in file {json_path}: {e}")
            return None

    @staticmethod
    def set_json_to_file(value: str, file_path: str, ensure_ascii: bool = False) -> Optional[bool]:
        """将字典转换成json字符串并写入文件.

        参数：
            value (str): 字典转化而来的json字符串.
            file_path (str): 要写入的文件路径.
            ensure_ascii (bool): 是否保证ascii字符在输出时不会转义.

        返回值：
            Optional[bool]: 成功时返回True；任何错误都返回None.

        注意：
            输入的value必须是有效的json格式字符串.
        """

        try:
            with open(file_path, "w", encoding="utf8")  as fws:
                json_data = json.loads(value)  # 尝试解析字符串，确认其为有效的JSON
                json.dump(json_data, fws, indent=4, sort_keys=True, ensure_ascii=ensure_ascii)
            return True
        except (OSError, json.JSONDecodeError) as e:
            # 若出现文件操作异常或者json解析异常，则返回None
            # raise IOError(f"Failed to write json file {file_path}: {e}") from e
            return None
    
    @staticmethod
    def get_json_value(file_path:str, key:str) -> json:
        """从json文件中获取给定键对应的值.

        参数：
            file_path (str): json文件路径.
            key (str): 需要获取的键名.

        返回值：
            Optional[Any]: 成功时返回对应的值；失败时返回None.

        注意：
            如果键不存在于json文件中，则返回None.
        """
        try:
            data = JsonUtils.load_json(file_path)  # 加载JSON文件内容
            if data is None:
                return None
            return data.get(key)  # 使用get避免KeyError
        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def set_value(file_path: str, key: str, value: Any) -> Optional[bool]:
        """在json文件中设置给定键的值.

        参数：
            file_path (str): JSON文件路径.
            key (str): 需要设置的键名.
            value (Any): 新的值.

        返回值：
            Optional[bool]: 成功时返回True；失败时返回None.
        """
        try:
            data = JsonUtils.load_json(file_path)  # 加载JSON文件内容
            if data is None:
                data = {}

            data[key] = value  # 更新或添加键值对
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except OSError:
            return None

    @staticmethod
    def loads_json_value(value: str) -> Optional[Any]:
        """将字符串转换为 JSON 对象，并提供错误处理和日志记录。

        参数：
            value (str): 需要转换的字符串。

        返回值：
            Any: JSON 对象。

        异常：
            ValueError: 如果输入的字符串不是合法的 JSON 格式。
        """
        try:
            return json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            # raise ValueError(f"Failed to convert value to json: {e}")
            return None

    @staticmethod
    def is_json(value:str) -> bool:
        """判断数据是否是json"""
        try:
            json.loads(value)  
        except (ValueError, TypeError, json.JSONDecodeError) as err:
            # raise ("The format is not json. msg: %s" % (err))
            # 捕获解析错误，并返回False
            return False
        # 解析成功，返回True
        return True
        
    def json_to_markdown(self, data, level=1):
        """
        将 JSON 数据或 JSON 字符串转换为 Markdown 文本
        :param data: JSON 数据（字典或列表）或 JSON 字符串
        :param level: 当前标题级别，默认为 1
        :return: Markdown 文本字符串
        """
        # 如果传入的是字符串，尝试将其解析为 Python 对象
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string")

        markdown_lines = []

        def add_heading(text, level):
            return f"{'#' * level} {text}"

        def process_dict(d, level):
            for key, value in d.items():
                if isinstance(value, dict):
                    markdown_lines.append(add_heading(key, level))
                    markdown_lines.append("")
                    process_dict(value, level + 1)
                elif isinstance(value, list):
                    markdown_lines.append(add_heading(key, level))
                    markdown_lines.append("")
                    process_list(value, level + 1)
                else:
                    markdown_lines.append(f"- **{key}**: {value}")
                    markdown_lines.append("")

        def process_list(lst, level):
            for index, item in enumerate(lst):
                if isinstance(item, dict):
                    markdown_lines.append(add_heading(f"Item {index + 1}", level))
                    markdown_lines.append("")
                    process_dict(item, level + 1)
                elif isinstance(item, list):
                    markdown_lines.append(add_heading(f"List {index + 1}", level))
                    markdown_lines.append("")
                    process_list(item, level + 1)
                else:
                    markdown_lines.append(f"- {item}")
                    markdown_lines.append("")

        if isinstance(data, dict):
            process_dict(data, level)
        elif isinstance(data, list):
            process_list(data, level)
        else:
            raise ValueError("Input data must be a dictionary, list, or valid JSON string")

        return "\n".join(markdown_lines)


if __name__ == "__main__":
    # 示例用法
    # 假设有一个名为config.json的JSON文件，我们需要更新键"example_key"的值为"new_value"
    success = JsonUtils.set_value("config.json", "example_key", "new_value")
    print("更新成功" if success else "更新失败")
