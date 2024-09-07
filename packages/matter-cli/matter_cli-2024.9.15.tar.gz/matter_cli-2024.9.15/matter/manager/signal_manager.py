# -*- encoding: utf-8 -*-
'''
@File		:	signal_manager.py
@Time		:	2024/01/18 14:09:42
@Author		:	dan
@Description:	信号管理器，用于存储信号的回调与组对应的关系
'''

from matter.group import Group
from matter.utils.singleton import singleton


@singleton
class SignalManager:
    '''
    信号管理器，用于存储信号的回调与组对应的关系
    '''
    def __init__(self) -> None:
        self.__signal_holder : dict[str, list] = {}
        pass


    def register_signal(self, group : Group, signal : str, callback) -> None:
        ''' 注册信号方法
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        # TODO 信号覆盖的问题

        callbacks = self.__signal_holder.get(signal)
        if not callbacks:
            callbacks = []
            self.__signal_holder[signal, callbacks]
        callbacks.append(callback)


    def unregister_signal(self, group : Group, signal : str, callback) -> None:
        ''' 注销信号方法
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        callbacks = self.__signal_holder.get(signal)
        if not callbacks:
            return True;
        callbacks.remove(callback)
        pass


    def post_signal(self, signal : str, value : any = None) -> None:
        ''' 发布信号
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        callbacks = self.__signal_holder.get(signal)
        if callbacks:
            for callback in callbacks:
                anno_len = len(callable.__annotations__)
                if anno_len == 0:
                    callback()
                elif anno_len == 1:
                    callback(signal)
                elif anno_len == 2:
                    callback(signal, value)
        pass