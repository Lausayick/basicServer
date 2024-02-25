#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : MySQL.py
@Time        : 2024/2/25 13:23
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    : Connect to project database.
@CoreLibrary :
"""
import pymysql
import socket
from dataclasses import dataclass


@dataclass
class MySQLInfo:
    """ Used for store information for connection to mysql database. """
    if socket.gethostname() == 'Lausayick':  # 本地调试ip
        ip = '122.51.25.144'
        port = 3306
    else:
        raise TypeError("Error Host Server!")
    username = 'private_domain'
    password = 'Lausayick_private_domain'
    database = 'private_domain'


def MySQL():
    """ Used for connecting to mysql database. """
    conn = pymysql.connect(host=MySQLInfo.ip, port=MySQLInfo.port, user=MySQLInfo.username, password=MySQLInfo.password, database=MySQLInfo.database)
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    # Please add a usage instance of the package.
    con, cur = MySQL()
