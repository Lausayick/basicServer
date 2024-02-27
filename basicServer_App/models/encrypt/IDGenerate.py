#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : IDGenerate.py
@Time        : 2024/2/26 10:54
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
import hashlib


def MD5(proclaim: str):
    """ MD5 方式生成 id """
    md5_object = hashlib.md5()
    md5_object.update(proclaim.encode('utf-8'))
    md5_result = md5_object.hexdigest()
    return md5_result


if __name__ == '__main__':
    # Please add a usage instance of the package.
    print(MD5('123asd测试'))
