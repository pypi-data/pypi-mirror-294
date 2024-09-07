# -*- encoding: utf-8 -*-
'''
@File		:	http.py
@Time		:	2024/01/05 15:35:11
@Author		:	dan
@Description:	matter 框架 http请求入口
'''


def get(url : str, query : list[str] = None, header : list[str] = None, cookies : list[str] = None) -> str | dict:
    ''' 发送get请求
    
    Parameters
    ----------
    url : str 请求的地址

    query : list[str] = None 请求时候发送的query

    header : list[str] = None 请求时候发送的header

    cookies : list[str] = None 请求时候发送的cookies
    
    Returns str
    -------
    '''
    
    pass


def post(url : str, query : list[str] = None, params : list[str] | dict = None, header : list[str] = None, cookies : list[str] = None) -> str | dict:
    ''' 发送post请求
    
    Parameters
    ----------
    url : str 请求的地址

    query : list[str] = None 请求时候发送的query

    params : list[str] | dict = None, 请求时候添加的参数，可以是表单，也可以是json

    header : list[str] = None 请求时候发送的header

    cookies : list[str] = None 请求时候发送的cookies
    
    Returns str
    -------
    '''
    
    pass




def put(url : str, query : list[str] = None, params : list[str] | dict = None, header : list[str] = None, cookies : list[str] = None) -> str | dict:
    ''' 发送put请求
    
    Parameters
    ----------
    url : str 请求的地址

    query : list[str] = None 请求时候发送的query

    params : list[str] | dict = None, 请求时候添加的参数，可以是表单，也可以是json

    header : list[str] = None 请求时候发送的header

    cookies : list[str] = None 请求时候发送的cookies
    
    Returns str
    -------
    '''
    
    pass




def delete(url : str, query : list[str] = None, params : list[str] | dict = None, header : list[str] = None, cookies : list[str] = None) -> str | dict:
    ''' 发送delete请求
    
    Parameters
    ----------
    url : str 请求的地址

    query : list[str] = None 请求时候发送的query

    params : list[str] | dict = None, 请求时候添加的参数，可以是表单，也可以是json

    header : list[str] = None 请求时候发送的header

    cookies : list[str] = None 请求时候发送的cookies
    
    Returns str
    -------
    '''
    
    pass