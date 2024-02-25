#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : PostgreSQL.py
@Time        : 2024/2/25 15:56
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
import psycopg2
import socket
from dataclasses import dataclass


@dataclass
class PostgreSqlInfo:
    """ Used for store information for connection to postgresql database. """
    if socket.gethostname() == 'Lausayick':  # 本地调试ip
        ip = '122.51.25.144'
        port = 18173
    else:
        raise TypeError("Error Host Server!")
    username = 'public_domain'
    password = 'Lausayick_public_domain'
    database = 'public_domain'


def PostgreSQL():
    """ Used for connecting to mysql database. """
    conn = psycopg2.connect(host=PostgreSqlInfo.ip, port=PostgreSqlInfo.port, user=PostgreSqlInfo.username, password=PostgreSqlInfo.password, database=PostgreSqlInfo.database)
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    # Please add a usage instance of the package.
    con, cur = PostgreSQL()
