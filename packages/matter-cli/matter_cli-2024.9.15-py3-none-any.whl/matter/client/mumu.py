# -*- encoding: utf-8 -*-
'''
@File		:	mumu.py
@Time		:	2024/01/11 11:54:40
@Author		:	dan
@Description:	mumu 模拟器 处理封装，包含开启/模拟模拟器，操作电脑需要预先安装mumu模拟器，并且设置好环境变量

仅适用于 mumu模拟器12或以上版本

所有资料参考 https://mumu.163.com/help/20230504/35047_1086360.html
'''
import os
import sys
if __name__ == '__main__':
    sys.path.append(".")
from matter.client.adb import Adb
import matter.utils.command as command


class MuMonitor:

    NOT_RUNNING = 'not_running'
    STARTING = 'starting_rom'
    STARTED = 'start_finished'


    @property
    def player_state(self) -> str:
        return self.__player_state
    
    @property
    def adb_host(self) -> str:
        if not self.__adb_host:
            self.refresh_adb_host()
        return self.__adb_host

    '''
    mumu模拟器封装
    '''
    def __init__(self, index : int) -> None:
        ''' 
        
        Parameters
        ----------
        index 模拟器序号
        
        Return
        ----------
        '''
        
        self.__index = index
        self.__player_state = MuMonitor.NOT_RUNNING
        self.__adb_host = None
        self.__started = False


    def start(self) -> None:
        ''' 开启模拟器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if self.__started:
            return;
        command.cmd("MuMuManager.exe", ["api", "-v", str(self.__index), "launch_player"])
        self.__started = True
        pass


    def refresh_state(self) -> bool:
        ''' 刷新模拟器状态
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool
        
        '''
        content = command.cmd_with_content("MuMuManager.exe", ["api", "-v", str(self.__index), "player_state"])
        if content.__contains__('state=start_finished'):
            self.__player_state = MuMonitor.STARTED
        if content.__contains__('state=starting_rom'):
            self.__player_state = MuMonitor.STARTING
        if content.__contains__('player not running'):
            self.__player_state = MuMonitor.NOT_RUNNING

        return self.__player_state;


    def refresh_adb_host(self) -> str:
        ''' 查询adb的端口
        
        Parameters
        ----------
        
        
        Returns
        -------
        str
        
        '''
        self.__adb_host = command.cmd_with_content("MuMuManager.exe", ["adb", "-v", str(self.__index)])
        return self.__adb_host

    def close(self) -> None:
        ''' 关闭模拟器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        command.cmd("MuMuManager.exe", ["api", "-v", str(self.__index), "shutdown_player"])
        self.__started = False;
        self.__adb_host = None;
        self.__player_state = MuMonitor.NOT_RUNNING
        pass


    def launch_app(self, package_name : str) -> None:
        ''' 启动app
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        command.cmd("MuMuManager.exe", ["api", "-v", str(self.__index), "launch_player", package_name])
        pass



if __name__ == '__main__':
    import time
    print("正在启动mumu模拟器")
    monitor = MuMonitor(index=0)
    monitor.start()

    ## 等待模拟器启动完毕
    not_ready = True
    while not_ready:
        all_ok = True
        if(monitor.player_state == MuMonitor.NOT_RUNNING or monitor.player_state == MuMonitor.STARTING):
            monitor.refresh_state()
            all_ok = False

        if all_ok:
            not_ready = False
        else:
            time.sleep(1)

    print("启动mumu模拟器完毕")
    print(monitor.adb_host)
    adb = Adb(monitor.adb_host, package_name='com.gonsin.conference.app')
    adb.connect()
    print(adb.is_installed('com.gonsin.conference.app'))
