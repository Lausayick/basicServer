#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : input.py
@Time        : 2024/2/25 21:13
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""


def getInputCheck(input_dict: dict, check_dict: dict, default_dict: dict = {}):
    """
    判断输入内容的格式输出
    check_dict = {
        key: 1,  1为必须 0为非必须
    }
    """
    errorMsg = None
    for key in check_dict:
        if check_dict[key] == 0:  # 非必要参数输入, 如无输入则默认
            if input_dict.get(key, None) is None and default_dict.get(key, None) is not None:
                input_dict[key] = default_dict[key]
        else:  # 必要参数输出
            if input_dict.get(key, None) is None:  # 没有输入, 报错
                errorMsg = f"请输入必要参数 '{key}'!"
                break

    return input_dict, errorMsg


if __name__ == '__main__':
    # Please add a usage instance of the package.
    pass
