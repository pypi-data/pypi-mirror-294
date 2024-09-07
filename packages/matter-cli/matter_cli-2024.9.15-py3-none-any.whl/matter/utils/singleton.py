# -*- encoding: utf-8 -*-
'''
@File		:	singleton.py
@Time		:	2024/01/05 09:57:01
@Author		:	dan
@Description:	单例的批注
'''


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner