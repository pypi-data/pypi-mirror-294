# -*- encoding: utf-8 -*-
'''
@File		:	system.py
@Time		:	2024/01/05 11:29:08
@Author		:	dan
@Description:	系统方法封装
'''
import re
import os
import platform


def exit(message : str, error_code = -1):
    '''
    退出程序并提示
    '''
    import sys
    print(message)
    sys.exit(error_code)



def isIP(str):
    """
    判断是否为IP
    """
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False



def isPort(str):
    """
    判断是否为端口
    """
    try:
        p = int(str)
        if p > 0 and p < 65500:
            return True
    except:
        return False
    return False


def download(url : str,  path : str):
    ''' 下载文件
    
    Parameters
    ----------
    url : str http路径

    path : str 本地路径
    
    Return
    ----------
    '''
    import wget
    wget.download(url, path)


def is_windows():
    '''
    当前是否为windows系统
    '''
    host_platform = platform.system().lower()
    if "windows" == host_platform:
        return True
    return False