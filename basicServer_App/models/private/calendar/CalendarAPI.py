#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : CalendarAPI.py
@Time        : 2024/2/25 19:27
@Author      : Lausayick
@Email       : lausayick@foxmail.com
@Software    : PyCharm
@Function    :
@CoreLibrary :
"""
import json
import datetime

from django.http import JsonResponse
from basicServer_App.models.standardization.result import ResultData
from basicServer_App.models.standardization.input import getInputCheck
from basicServer_App.models.private.calendar import CalendarDB
from basicServer_App.models.encrypt import IDGenerate
DEFAULT_COLOR = 'grey'
PUBLIC_USERID = '1314'

def calendar_manage(request):
    # 处理返回的结果并判断 doMethod 的内容
    user_id = '520'
    resultData = ResultData()
    data_request = json.loads(request.body)
    doMethod = data_request.get('doMethod', None)
    if not doMethod:
        resultData.errorData(errorMsg="请输入参数 'doMethod'!")
    if doMethod == 'getCalendarGroup':  # 获取分组
        # 验证必要输入参数
        check_dict = {
            'public': 0,
            'calendar_type': 1,
        }
        default_dict = {
            'public': True,
        }
        data_request, errorMsg = getInputCheck(input_dict=data_request, check_dict=check_dict,
                                               default_dict=default_dict)
        if errorMsg:
            resultData.errorData(errorMsg=errorMsg)
            return JsonResponse(resultData.to_Dict())

        # 数据格式检测
        if data_request["public"]:
            user_id = PUBLIC_USERID
        if data_request['calendar_type'] not in ['to-do']:
            resultData.errorParam(param="calendar_type")
            return JsonResponse(resultData.to_Dict())

        # 获取数据并返回
        resultData.data = CalendarDB.getCalendarGroup(user_id=user_id, data=data_request)

    elif doMethod == 'addCalendarGroup':  # 增添分组
        # 验证必要输入参数
        check_dict = {
            'public': 0,
            'group_name': 1,
            'calendar_type': 1,
            'color': 0,
        }
        default_dict = {
            'public': False,
            'color': DEFAULT_COLOR,
        }
        data_request, errorMsg = getInputCheck(input_dict=data_request, check_dict=check_dict,
                                               default_dict=default_dict)
        if errorMsg:
            resultData.errorData(errorMsg=errorMsg)
            return JsonResponse(resultData.to_Dict())

        # 处理输入数据内容
        if data_request['public']:
            user_id = PUBLIC_USERID
        if CalendarDB.checkGroupExists(user_id=user_id, group_name=data_request['group_name']):
            resultData.errorData(errorMsg="新建分组已经存在！")
            return JsonResponse(resultData.to_Dict())
        data_request['id'] = "group_" + IDGenerate.MD5(proclaim=user_id + data_request['group_name'] + str(datetime.datetime.now()))
        if CalendarDB.checkGroupIdExists(group_id=data_request['id']):
            resultData.errorData(errorMsg="新建id已经存在！")
            return JsonResponse(resultData.to_Dict())

        # 插入新的测试结果
        if not CalendarDB.insertGroup(user_id=user_id, data=data_request):
            resultData.errorData(errorMsg="数据库出错，请稍后重试！")
            return JsonResponse(resultData.to_Dict())

        resultData.group_id = data_request['id']

    elif doMethod == 'deleteCalendarGroup':  # 删除分组
        # 验证必要输入参数
        check_dict = {
            'group_id': 1,
            'calendar_type': 1
        }
        default_dict = {}
        data_request, errorMsg = getInputCheck(input_dict=data_request, check_dict=check_dict, default_dict=default_dict)
        if errorMsg:
            resultData.errorData(errorMsg=errorMsg)
            return JsonResponse(resultData.to_Dict())

        # 验证输入内容
        if data_request['calendar_type'] not in ['to-do']:
            resultData.errorParam(param="calendar_type")
            return JsonResponse(resultData.to_Dict())
        if not CalendarDB.checkGroupIdExistsWithType(group_id=data_request['group_id'], calendar_type=data_request['calendar_type']):
            resultData.errorData(errorMsg="目标删除 group_id 不存在！")
            return JsonResponse(resultData.to_Dict())

        # 删除对应的分组并对该类别重新排序 order
        if not CalendarDB.deleteCalendarGroup(group_id=data_request['group_id']) or not CalendarDB.reorderCalendarGroup(user_id=user_id, calendar_type=data_request['calendar_type']):
            resultData.errorData(errorMsg="数据库操作错误，请稍后重试！")
            return JsonResponse(resultData.to_Dict())

    elif doMethod == 'changeCalendarGroup':  # 修改分组信息
        # 验证必要输入参数
        check_dict = {
            'group_id': 1,
            'calendar_type': 1,
            'group_name': 0,
            'color': 0,
            'group_order': 0,
        }
        default_dict = {}
        data_request, errorMsg = getInputCheck(input_dict=data_request, check_dict=check_dict, default_dict=default_dict)
        if errorMsg:
            resultData.errorData(errorMsg=errorMsg)
            return JsonResponse(resultData.to_Dict())

        # 验证输入内容
        if data_request['calendar_type'] not in ['to-do']:
            resultData.errorParam(param="calendar_type")
            return JsonResponse(resultData.to_Dict())
        if not (data_request.get("group_name", None) or data_request.get("group_order", None) or data_request.get("color", None)):
            resultData.errorData(errorMsg="请输入要修改的内容！")
            return JsonResponse(resultData.to_Dict())
        if not CalendarDB.checkGroupIdExistsWithType(group_id=data_request['group_id'], calendar_type=data_request['calendar_type']):
            resultData.errorData(errorMsg="目标修改 group_id 不存在！")
            return JsonResponse(resultData.to_Dict())

        # 提交修改
        if not CalendarDB.updateCalendarGroup(data=data_request):
            resultData.errorData(errorMsg="数据库操作出错，请稍后重试！")
            return JsonResponse(resultData.to_Dict())

    elif doMethod == 'getCalendarData':  # 获取历史数据
        pass

    elif doMethod == 'addCalendar':  # 新增待办事项
        # 验证必要输入参数
        calendar_type = data_request.get("calendar_type", None)
        if calendar_type in ['to-do', ]:
            check_dict = {
                'calendar_group_id': 1,
                'title': 1,
                'description': 0,
                'notes': 0,
                'target_date': 0,
                'is_alarm': 0,
            }
            if data_request.get("is_alarm"):
                check_dict.update({
                    'alarm_time': 1,
                    'alarm_interval': 1,
                    'music_id': 1
                })
        elif calendar_type in ['matters', ]:
            check_dict = {
                'calendar_group_id': 1,
                'title': 1,
                'description': 0,
                'target_date': 0,
                'notes': 0,
                'is_alarm': 0,
            }
            if data_request.get("is_alarm"):
                check_dict.update({
                    'alarm_time': 1,
                    'alarm_interval': 1,
                    'music_id': 1
                })
        else:
            resultData.errorParam(param="calendar_type")
            return JsonResponse(resultData.to_Dict())
        default_dict = {
            'is_alarm': False,
        }
        data_request, errorMsg = getInputCheck(input_dict=data_request, check_dict=check_dict, default_dict=default_dict)
        if errorMsg:
            resultData.errorData(errorMsg=errorMsg)
            return JsonResponse(resultData.to_Dict())

        # 验证输入内容
        if not CalendarDB.checkGroupIdExistsWithType(group_id=data_request['calendar_group_id'], calendar_type=calendar_type):
            resultData.errorData(errorMsg="目标 group_id 不存在！")
            return JsonResponse(resultData.to_Dict())
        # TODO: Music Id 的存在性校验
        if CalendarDB.checkCalendarTitleExists(group_id=data_request['calendar_group_id'], title=data_request['title']):
            resultData.errorData(errorMsg="添加的事项在本分组中已经存在！")
            return JsonResponse(resultData.to_Dict())

        # 生成 id 并且插入数据
        data_request['id'] = calendar_type + "_" + IDGenerate.MD5(proclaim=user_id + data_request['title'] + str(datetime.datetime.now()))
        if CalendarDB.checkCalendarIdExists(calendar_id=data_request['id']):
            resultData.errorData(errorMsg="生成 id 重复!")
            return JsonResponse(resultData.to_Dict())
        if not CalendarDB.insertCalendar(user_id=user_id, data=data_request):
            resultData.errorData(errorMsg="数据库操作出错，请稍后重试！")
            return JsonResponse(resultData.to_Dict())

    elif doMethod == 'deleteCalendar':  # 删除待办事项
        pass

    elif doMethod == 'changeCalendar':  # 修改表项信息
        pass

    else:
        resultData.errorData(errorMsg="参数 'doMethod' 请求类别不存在!")

    return JsonResponse(resultData.to_Dict())


if __name__ == '__main__':
    # Please add a usage instance of the package.
    pass
