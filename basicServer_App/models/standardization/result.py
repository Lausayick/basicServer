#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : result.py
@Time        : 2024/2/25 19:53
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
from dataclasses import dataclass


class ResultData(object):
    """ Used for return data used. """
    def __init__(self, errorCode='000000', errorMsg='', errorFlag=False, data={}):
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        self.errorFlag = errorFlag
        self.data = data

    def errorData(self, errorCode='000001', errorMsg='', errorFlag=True):
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        self.errorFlag = errorFlag

    def errorParam(self, errorCode='000002', param='', errorFlag=True):
        self.errorCode = errorCode
        self.errorMsg = f"参数 '{param}' 取值错误!"
        self.errorFlag = errorFlag

    def loginTimeOut(self, errorCode='001001', errorMsg='登录已超时，请重新登录!', errorFlag=True):
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        self.errorFlag = errorFlag

    def to_Dict(self):
        """ 将类转换为字典返回，并且将非标志位信息归并到 data """
        data = {}
        delete_keys = []
        for key in self.__dict__:
            if key in ['data']:
                if not isinstance(self.__dict__[key], dict):
                    data['data'] = self.__dict__[key]
                else:
                    for key_item in self.__dict__[key].keys():
                        data[key_item] = self.__dict__[key][key_item]
            if key not in ['data', 'errorCode', 'errorMsg', 'errorFlag']:
                data[key] = self.__dict__[key]
                delete_keys.append(key)
        for key in delete_keys:
            self.__dict__.pop(key)
        self.data = data

        return self.__dict__


if __name__ == '__main__':
    # Please add a usage instance of the package.
    pass
