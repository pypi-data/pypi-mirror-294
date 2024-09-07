# -*- encoding: utf-8 -*-
'''
@File		:	proxy_server.py
@Time		:	2024/01/05 15:45:00
@Author		:	dan
@Description:	代理服务器，通过matter命令行开启代理服务
'''

import socket
import time
import selectors
import threading

from matter.utils.console import print_error, print_info

class ProxyServer:


    @property
    def started(self) -> bool:
        ''' 
        线程是否已开始
        '''
        
        return self.__running

    '''
    代理服务器，监听指定的端口，接收主测试机的指令
    '''
    def __init__(self, port : int = 6666, callback = None , quiet : bool=False) -> None:
        ''' 
        Parameters
        ----------
        port : int = 6666 代理服务器监听的端口

        callback : function[socket.socket, str] 监听接收的回调
        
        Return
        ----------
        '''

        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)
        self.__started = False
        self.__selector = selectors.DefaultSelector()
        self.__last = {}
        self.__quiet = quiet
        self.__socket.settimeout(1)
        self.__callback = callback

        self.__thread = threading.Thread(target=self.run)
        self.__running = False
        pass


    def __accept(self, sock : socket.socket, mask):
        ''' socket连接的回调
        Parameters
        ----------
        sock 也就是 self.__socket

        mask 
        
        Return
        ----------
        '''
        
        conn, address = sock.accept()  # Should be ready
        print_info(f'    来自 {conn.getpeername()}，连接成功')
        conn.setblocking(False)  #设置成非阻塞
        self.__last[str(conn)] = b''
        self.__selector.register(conn, selectors.EVENT_READ, self.__read) #conn绑定的是read


    def __read(self, conn : socket.socket, mask):
        ''' 读取数据的回调
        
        Parameters
        ----------
        conn 连接

        
        Return
        ----------
        '''
        
        try:
            data = conn.recv(1000)  # Should be ready
            if data:
                data_list = str((self.__last[str(conn)] + data), encoding='utf8').split("\n")
                self.__last[str(conn)] = bytes(data_list[-1], encoding='utf8')
                data = data_list[:-1]
                if data:
                    for line in data:
                        print_info(f'    来自 {conn.getpeername()}， 接收 {line}')
                        if self.__callback:
                            self.__callback(conn, line)
            else:
                print_info(f'    来自 {conn.getpeername()}，正常关闭')
                conn.close()
                self.__selector.unregister(conn)

            ## TODO 处理接收到的内容
            # if not data:
            #     raise Exception
            # print('echoing', repr(data), 'to', conn)
            # conn.send(data)  # Hope it won't block
        except Exception as e:
            print_error(f'    来自 {conn.getpeername()}，意外关闭')
            print_error(f'    ', e)
            conn.close()
            self.__selector.unregister(conn)  #解除注册
        


    def start(self) -> None:
        ''' 开始监听
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__running = True
        self.__thread.start()
        pass

    def close(self) -> None:
        ''' 结束监听
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__running = False
        pass


    def run(self) -> None:
        ''' 开启代理服务器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if self.__started:
            return;
        self.__started = True

        sock = self.__socket
        sock.bind(('0.0.0.0', self.__port))
        sock.listen(2)
        sock.setblocking(False)
        sel = self.__selector
        sel.register(sock, selectors.EVENT_READ, self.__accept)
        if not self.__quiet:
            print(f"代理服务器开始监听，监听端口{self.__port}\n")
        while self.__running:
            try:  
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
            except Exception as e:  #捕捉错误
                print (e)
                time.sleep(4)  #每4秒打印一个捕捉到的错误

        if not self.__quiet:
            print(f"代理服务器结束监听\n")
        sock.close()
        sel.close()
        pass


if __name__ == '__main__':
    server = ProxyServer()
    server.start()
    time.sleep(1000)