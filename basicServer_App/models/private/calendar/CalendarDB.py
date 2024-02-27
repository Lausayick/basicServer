#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : CalendarDB.py
@Time        : 2024/2/25 18:30
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
import datetime
from basicServer_App.models.database.MySQL import MySQL_Connect
PUBLIC_USERID = '1314'


def checkGroupExists(user_id: str, group_name: str):
    """
    Function:
        检验待办事项的分组是否存在
    Return:
        True: 已经存在分组
        False: 不存在目标分组
    """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar_group cg
        WHERE cg.userid=%s and cg.group_name=%s
        '''
        res = cur.execute(query_sql, [user_id, group_name])
        data = cur.fetchall()[0][0]
        if data >= 1:
            return True
        return False
    except Exception as except_error:
        print(except_error)
        return True
    finally:
        cur.close()
        con.close()


def checkGroupIdExists(group_id):
    """
    Function:
        检验待办事项的分组生成的 id 是否存在
    Return:
        True: 已经存在分组
        False: 不存在目标分组
    """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar_group cg
        WHERE cg.id=%s
        '''
        res = cur.execute(query_sql, [group_id])
        data = cur.fetchall()[0][0]
        if data >= 1:
            return True
        return False
    except Exception as except_error:
        print(except_error)
        return True
    finally:
        cur.close()
        con.close()


def checkGroupIdExistsWithType(group_id: str, calendar_type: str):
    """
    Function:
        检验待办事项的分组生成的 id 是否存在, 并结合对应的 calendar type
    Return:
        True: 已经存在分组
        False: 不存在目标分组
    """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar_group cg
        WHERE cg.id=%s and cg.calendar_type=%s
        '''
        res = cur.execute(query_sql, [group_id, calendar_type])
        data = cur.fetchall()[0][0]
        if data >= 1:
            return True
        return False
    except Exception as except_error:
        print(except_error)
        return True
    finally:
        cur.close()
        con.close()


def checkCalendarTitleExists(group_id: str, title: str):
    """ 检查同组 title 是否存在 """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar c
        WHERE c.title=%s and c.calendar_group_id=%s
        '''
        res = cur.execute(query_sql, [title, group_id])
        data = cur.fetchall()[0][0]
        if data >= 1:
            return True
        return False
    except Exception as except_error:
        print(except_error)
        return True
    finally:
        cur.close()
        con.close()


def checkCalendarIdExists(calendar_id):
    """ 检查 calendar_id 是否存在 """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar c
        WHERE c.id=%s
        '''
        res = cur.execute(query_sql, [calendar_id])
        data = cur.fetchall()[0][0]
        if data >= 1:
            return True
        return False
    except Exception as except_error:
        print(except_error)
        return True
    finally:
        cur.close()
        con.close()


def get_data():
    con, cur = MySQL_Connect()


def getNewGroupOrder(user_id: str) -> int:
    """ 获取最新的分组的 order 排序 """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT COUNT(1)
        FROM calendar_group cg
        WHERE cg.userid=%s
        '''
        res = cur.execute(query_sql, [user_id])
        data = cur.fetchall()[0][0]
        return data + 1
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def getCalendarGroup(user_id: str, data: dict):
    """ 获取待办事项分组 """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT cg.id, cg.group_name, cg.color, cg.group_num
        FROM calendar_group cg
        WHERE cg.userid=%s and cg.calendar_type=%s
        ORDER BY group_order ASC
        '''
        res = cur.execute(query_sql, [user_id, data['calendar_type']])
        data = []
        for data_item in cur.fetchall():
            print(data_item)
            data_one = {}
            for idx, key in enumerate(cur.description):
                data_one[key[0]] = data_item[idx]
            data.append(data_one)
        print(data)
        return data
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def updateCalendarGroup(data: dict):
    """ 修改待办事项的分组信息 """
    con, cur = MySQL_Connect()
    try:
        for key in data.keys():
            if key not in ['doMethod', 'group_id', 'calendar_type']:
                update_sql = f'''
                UPDATE calendar_group cg
                SET cg.{key}=%s
                WHERE cg.id=%s 
                '''
                res = cur.execute(update_sql, [data[key], data['group_id']])
        con.commit()
        return True
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def insertGroup(user_id, data):
    """
    Function:
        插入新的分组
    Return:
        True: 执行完成
        False: 数据库执行出错
    """
    con, cur = MySQL_Connect()
    try:
        insert_sql = '''
        INSERT INTO calendar_group
        (id, userid, group_name, color, group_order, group_num, calendar_type)
        VALUES (%s, %s, %s, %s, %s, 0, %s)
        '''
        res = cur.execute(insert_sql, [data['id'], user_id, data['group_name'], data['color'], getNewGroupOrder(user_id=user_id), data['calendar_type']])
        con.commit()
        return True
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def insertCalendar(user_id, data):
    """ 插入待办事项的数据 """
    con, cur = MySQL_Connect()
    try:
        insert_sql = '''
        INSERT INTO calendar
        (id, date, calendar_type, calendar_group_id, title, description, target_date, notes, is_alarm, alarm_interval, alarm_time, music_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        res = cur.execute(insert_sql, [data['id'], datetime.datetime.now(), data['calendar_type'], data['calendar_group_id'], data['title'], data.get('description', None), data.get('target_date', None), data.get('notes', None), data.get('is_alarm', None), data.get('alarm_interval', None), data.get('alarm_time', None), data.get('music_id', None)])
        con.commit()
        return True
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def deleteCalendarGroup(group_id):
    """ 删除待办事项的分组 """
    con, cur = MySQL_Connect()
    try:
        delete_sql = '''
        DELETE FROM calendar_group cg
        WHERE cg.id=%s
        '''
        res = cur.execute(delete_sql, [group_id])
        con.commit()
        return True
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


def reorderCalendarGroup(user_id: str, calendar_type: str):
    """ 重新排序 order 字段 """
    con, cur = MySQL_Connect()
    try:
        query_sql = '''
        SELECT id
        FROM calendar_group cg
        WHERE cg.calendar_type=%s and cg.userid=%s
        ORDER BY group_order ASC
        '''
        res = cur.execute(query_sql, [calendar_type, user_id])
        for idx, data_item in enumerate(cur.fetchall()):
            update_sql = '''
            UPDATE calendar_group cg
            SET cg.group_order=%s
            WHERE cg.id=%s
            '''
            cur.execute(update_sql, [idx, data_item[0]])
        con.commit()
        return True
    except Exception as except_error:
        print(except_error)
        return False
    finally:
        cur.close()
        con.close()


if __name__ == '__main__':
    # Please add a usage instance of the package.
    # get_data()
    data = {
        'calendar_type': 'to-do list',  # matters
        'id': 'todo-123',
        'date': datetime.datetime.now(),
        'calendar_group': 'test'
    }
    print(reorderCalendarGroup(user_id='1314', calendar_type='to-do'))