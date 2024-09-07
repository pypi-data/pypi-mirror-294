# -*- encoding: utf-8 -*-
'''
@File		:	proxy_manager.py
@Time		:	2024/01/10 14:59:57
@Author		:	dan
@Description:	代理处理逻辑
'''


from matter.proxy.proxy_client import ProxyClient
from matter.utils.singleton import singleton
import threading
import matter.utils.system_utils as system_utils

@singleton
class ProxyManager:
    ''' 
    存储所有远程代理连接
    '''
    

    
    def __init__(self) -> None:
        ''' 
        
        Parameters
        ----------
        
        
        '''
        self.__server = None;
        self.__proxy_devices : set[str] = set();
        self.__proxy_clients : dict[str, ProxyClient] = {};
        ''' 
        远程的服务器列表        
        '''
        
        pass


    def append_proxy(self, remote_address : str) -> None:
        ''' 添加远程的设备
        
        Parameters
        ----------
        remote_address : str 格式为 IP:Port 或者 IP
        
        Returns
        -------
        None
        
        '''
        if not remote_address.__contains__(":"):
            remote_address = remote_address + ":6666"
        self.__proxy_devices.add(remote_address)


    def connect_to_proxy(self, waiting : bool = True) -> None:
        ''' 连接到远程服务
        
        Parameters
        ----------
        waiting : bool 等待连接全部完成
        
        Returns
        -------
        None
        
        '''
        if not self.__proxy_devices:
            return
        
        cond = threading.Condition(len(self.__proxy_devices))
        for host in self.__proxy_devices:
            ip, port = host.split(":")
            client = ProxyClient(ip, port, cond)
            self.__proxy_clients[host] = client
            client.start()

        if waiting:
            if not cond.wait(10):
                not_connect_host = []
                for client in self.__proxy_clients.values():
                    if not client.connected:
                        not_connect_host.append(client.host)

                if not_connect_host:
                    not_connect_host = "\n".join(not_connect_host)
                    system_utils.exit(f'无法连接到代理服务器，请检查远程的设备是否运行了 matter run_proxy 命令，代理服务器包含如下：\n {not_connect_host}')


    def send_to_proxy(self, host : str, msg : str | dict) -> None:
        ''' 发送消息到远程服务
        
        Parameters
        ----------
        host : str 远程服务器的地址
        
        msg : str | dict 发送的内容
        
        Returns
        -------
        None
        
        '''
        
        if not self.__proxy_devices:
            return
        
        client = self.__proxy_clients[host]
        if client:
            client.write(msg)


PROXY_MANAGER = ProxyManager()