# -*- encoding: utf-8 -*-
'''
@File		:	http.py
@Time		:	2024/01/05 10:30:12
@Author		:	dan
@Description:	http请求封装类，使用的是原生的 requests 模块
'''

import requests

class Http:
    '''
    http 请求封装类，包含get、post、delete、put等方法
    '''

    def __init__(self, host : str, 
                 headers : list[str] = None, 
                 querys : list[str] = None, 
                 cookies : list[str] = None,
                 params : list[str] = None,
                 ) -> None:
        ''' 
        Parameters
        ----------
        host : str 访问服务器的前缀

        client_count : int 并发线程数量

        headers : list[str] 请求时候需要添加额外的header值

        querys : list[str] 请求时候需要额外添加的query值
        '''
        self.__host = host
        self.__headers = headers
        self.__querys = querys
        self.__cookies = cookies
        self.__params = params
        pass


    def __handle_headers(self, headers : dict) -> dict:
        ''' header处理，封装
        
        Parameters
        ----------
        
        
        Returns
        -------
        dict
        
        '''
        
        if self.__headers:
            if not headers:
                headers = {}
            for s in self.__headers:
                key, value = s.split("=")
                if not headers.__contains__(key):
                    headers[key] = value
        return headers


    def __handle_cookies(self, cookies : dict) -> dict:
        ''' cookies处理，封装
        
        Parameters
        ----------
        
        
        Returns
        -------
        dict
        
        '''
        
        if self.__cookies:
            if not cookies:
                cookies = {}
            for s in self.__cookies:
                key, value = s.split("=")
                if not cookies.__contains__(key):
                    cookies[key] = value
        return cookies


    def __handle_params(self, params : dict) -> dict:
        ''' params处理，封装
        
        Parameters
        ----------
        
        
        Returns
        -------
        dict
        
        '''
        
        if self.__params:
            if not params:
                params = {}
            for s in self.__params:
                key, value = s.split("=")
                if not params.__contains__(key):
                    params[key] = value
        return params
    
    


    def __handle_query(self, url : str) -> dict:
        ''' cookies处理，封装
        
        Parameters
        ----------
        
        
        Returns
        -------
        dict
        
        '''
        
        if self.__querys:
            for s in self.__querys:
                if not url.__contains__("?"):
                    url = "?" + s
                else :
                    url = "&" + s
        return url


    def get(self, url : str = None, params : dict = None, headers : dict = None, cookies : dict = None) -> requests.Response:
        ''' 
        ### 发送get请求

        #### Parameters
        url : str = None 请求的url

        params : dict = None 请求附带的参数
          
        #### Returns
        str | map
        
        '''
        
        headers = self.__handle_headers(headers=headers)
        cookies = self.__handle_cookies(cookies=cookies)
        url = self.__handle_query(url=url)
        params = self.__handle_params(params=params)

        return requests.get(url = self.__host + url, params=params, headers=headers, cookies=cookies)