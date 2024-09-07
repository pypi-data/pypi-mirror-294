# -*- encoding: utf-8 -*-
'''
@File		:	run_proxy.py
@Time		:	2024/01/10 16:47:18
@Author		:	dan
@Description:	命令行运行代理服务器的入口位置
'''

import argparse
import time
import signal
import sys

from matter.proxy.proxy_server import ProxyServer
from matter.proxy.proxy_web_server import ProxyWebServer

def run(args) -> None:
    ''' 
    执行命令行 matter run_proxy 之后进入该方法

    args 只获取 matter run_proxy 后面的内容
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    parser = argparse.ArgumentParser("matter run_proxy", description="运行代理", add_help=False)
    parser.add_argument('-p', '--port', help='指定监听端口', type=int, default=6666)
    parser.add_argument('-wp', '--web_port', help='指定web服务器监听端口', type=int, default=6667)
    parser.add_argument('-h', '--help', help='查看帮助', default=False, action="store_true")
    result = parser.parse_args(args)

    if result.help:
        parser.print_help()
        return 0;

    
    server = ProxyServer(result.port, quiet=True)
    web_server = ProxyWebServer(result.web_port, quiet=True)
    server.start()
    web_server.start()

    def signal_handler(signal, frame):
        server.close()
        web_server.close()
        sys.exit(0)



    print(f"\
你已启动了代理服务器，监听地址为 0.0.0.0:{result.port}\n\
web服务器监听地址为 0.0.0.0:{result.web_port}\n\
点击 ctrl + c 退出监听")
    print("")

    signal.signal(signal.SIGINT, signal_handler)
    while True:
        time.sleep(1)
