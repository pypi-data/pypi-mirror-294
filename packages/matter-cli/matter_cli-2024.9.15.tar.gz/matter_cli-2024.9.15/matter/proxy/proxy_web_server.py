# -*- encoding: utf-8 -*-
'''
@File		:	proxy_web_server.py
@Time		:	2024/01/10 17:00:14
@Author		:	dan
@Description:	代理服务器的轻量级web服务，用于传递文件
'''

import bottle
import threading
import os
import pathlib

class ProxyWebServer(bottle.Bottle):

    @property
    def started(self) -> bool:
        return self.__started

    def __init__(self, port : int = 6667, upload_dir : str = './upload', async_run : bool = True, quiet = False) -> None:
        super().__init__()
        ''' 创建web服务器
        
        Parameters
        ----------
        port : int web服务器监听端口

        upload_dir : str 文件上传后存放的位置

        async_run : bool 是否异步运行
        
        '''
        self.__upload_dir = upload_dir
        self.__thread = threading.Thread(target=self.run)
        self.__started = False
        self.__port = port
        self.__async_run = async_run
        self.route('/check_file', callback=self.check_file, method='GET')
        self.route('/upload', callback=self.upload, method='POST')
        self.__quite = quiet
        pass


    def start(self) -> None:
        ''' 开启web服务
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__started = True;
        if self.__async_run:
            self.__thread.start()
            return;
        self.run()


    def run(self) -> None:
        ''' 运行服务器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        bottle.run(app=self, port=self.__port, host='0.0.0.0', quiet=self.__quite)
        


    @bottle.route('/check_file', mothod='GET')
    def check_file(self) -> str | dict:
        ''' 检查文件是否存在
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        md5 = bottle.request.params['md5']
        if not md5:
            return {
                "data" : False,
                "error_code": 0
            }
        
        exist = self.__check_file_exist(md5)
        return {
                "data" : exist,
                "error_code": 0
            }


    def __check_file_exist(self, md5: str) -> bool:
        ''' 
        根据文件的md5检查文件是否存在
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        return os.path.isdir(f"{self.__upload_dir}/{md5}")

    # @bottle.route('/upload', mothod='POST')
    def upload(self) -> None:
        ''' 文件上传入口
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        uploadfile = bottle.request.files.get('file')  # 获取上传的文件
        md5 = bottle.request.params['md5']
        local_dir = f"{self.__upload_dir}/{md5}";
        if not os.path.isdir(local_dir):
            p = pathlib.Path(local_dir)
            if not p.exists():
                p.mkdir(parents=True)
        uploadfile.save(f"{local_dir}/{uploadfile.origin_name}", overwrite=True)
        return {
                "error_code": 0
            }


if __name__ == '__main__':
    web = ProxyWebServer(async_run=False, port=16667)
    web.start()