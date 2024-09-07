# -*- encoding: utf-8 -*-
'''
@File		:	socket.py
@Time		:	2024/09/03 10:20:07
@Author		:	dan
@Description:	测试socket
'''
from matter.manager.group_manager import GroupManager

def write(msg : str | dict | bytes):
    '''
    所有的 socket 连接发送数据
    '''
    client = GroupManager().current_client()
    client.socket.write(msg)