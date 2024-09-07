# -*- encoding: utf-8 -*-
'''
@File		:	client_manager.py
@Time		:	2024/01/05 09:53:43
@Author		:	dan
@Description:	管理虚拟客户端的类
'''

from matter.client import Client
from matter.utils.singleton import singleton

@singleton
class ClientManager:

    @property
    def clients(self) -> list[Client] :
        return self.__clients
    
    def __init__(self) -> None:
        pass