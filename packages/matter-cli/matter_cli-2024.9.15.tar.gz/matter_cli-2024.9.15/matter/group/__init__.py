# -*- encoding: utf-8 -*-
'''
@File		:	group.py
@Time		:	2024/01/05 10:03:26
@Author		:	dan
@Description:	组对象
'''


from typing import Literal
from matter.manager.case_manager import CaseManager
import matter.utils.system_utils as system_utils
import warnings
import matter.utils.console as console

class AndroidSetting:
    '''
    安卓端的设置
    '''

    @property
    def apk(self) -> str:
        '''
        安卓端apk位置
        '''
        return self.__apk

    @property
    def package_name(self) -> str:
        '''
        需要测试的包名
        '''
        return self.__package_name
        

    @property
    def android_test(self) -> str:
        '''
        使用apk测试还是 package_name测试
        '''
        return self.__android_test
        

    @property
    def uninstall(self) -> bool:
        '''
        安装apk之前是否卸载原来的apk
        '''
        return self.__uninstall
        

    @property
    def restart(self) -> bool:
        '''
        每次测试是否重启应用
        '''
        return self.__restart
        

    @property
    def targets(self) -> list[str]:
        '''
        可以测试的目标设备
        '''
        return self.__targets
        

    @property
    def mumu(self) -> int:
        '''
        开启的mumu模拟器数量
        '''
        return self.__mumu

    def __init__(self, apk, package_name, android_test, uninstall, restart, targets : list[str], mumu : int) -> None:
        self.__apk = apk
        self.__package_name = package_name
        self.__android_test = android_test
        self.__uninstall = uninstall
        self.__restart = restart
        self.__targets = targets
        self.__mumu = mumu




class BrowserSetting:
    '''
    浏览器的设置
    '''

    @property
    def url(self) -> str:
        '''
        浏览器打开时候第一个页面
        '''
        return self.__url

    @property
    def window_size(self) -> str:
        '''
        浏览器打开的大小
        '''
        return self.__window_size

    @property
    def client_count(self) -> int:
        '''
        '''
        return self.__client_count

    @property
    def targets(self) -> list[str]:
        '''
        '''
        return self.__targets

    @property
    def arguments(self) -> list[str]:
        '''
        '''
        return self.__arguments
        

    def __init__(self, url, window_size, 
            client_count : int,
            targets : list[str],
            arguments : list[str]) -> None:
        self.__url = url
        self.__window_size = window_size
        self.__client_count = client_count
        self.__targets = targets
        self.__arguments = arguments





class DesktopSetting:
    '''
    桌面程序的设置
    '''

    @property
    def restart(self) -> bool:
        '''
        开启测试时是否重新启动应用
        '''
        return self.__restart

    @property
    def window_size(self) -> str:
        '''
        测试程序窗口大小
        '''
        return self.__window_size

    @property
    def bin(self) -> str:
        '''
        测试程序位置
        '''
        return self.__bin
        
        

    def __init__(self, restart, window_size, bin) -> None:
        self.__restart = restart
        self.__window_size = window_size
        self.__bin = bin


class HttpSetting:
    '''
    Http请求的设置
    '''

    @property
    def host(self) -> str:
        return self.__host

    @property
    def client_count(self) -> int:
        return self.__client_count

    def __init__(self, host : str, client_count : int) -> None:
        self.__host = host
        self.__client_count = client_count


class SocketSetting:
    '''
    Socket请求的设置
    '''
    @property
    def host(self) -> str:
        return self.__host
    @property
    def protocol(self) -> str:
        return self.__protocol
    @property
    def ip(self) -> str:
        return self.__ip
    @property
    def port(self) -> int:
        return self.__port
    @property
    def client_count(self) -> int:
        return self.__client_count

    def __init__(self, host : str, protocol : str, ip : str, port : int, client_count :int) -> None:
        self.__host = host
        self.__protocol = protocol
        self.__ip = ip
        self.__port = port
        self.__client_count = client_count

        

class MqttSetting:
    '''
    Mqtt的设置
    '''
    @property
    def host(self) -> str:
        return self.__host
    
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def password(self) -> str:
        return self.__password
    
    @property
    def subscribe_topics(self) -> str:
        return self.__subscribe_topics
    
    @property
    def keepalive(self) -> int:
        return self.__keepalive
    
    @property
    def transport(self) -> int:
        return self.__transport
    
    @property
    def clean_start(self) -> bool:
        return self.__clean_start
    
    @property
    def client_count(self) -> int:
        return self.__client_count
    
    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def port(self) -> int:
        return self.__port
    
    @property
    def protocol(self) -> str:
        return self.__protocol

    def __init__(self, host : str, 
                 client_count : int,
                 ip : str,
                 port : int,
                 protocol : str,
                 username : str, 
                 password : str, 
                 subscribe_topics : list[str] = [], 
                 keepalive : int = 60,
                 clean_start : bool = True,
                 transport : Literal["tcp", "websockets", "unix"] = 'tcp', ) -> None:
        self.__host = host
        self.__username = username
        self.__password = password
        self.__subscribe_topics = subscribe_topics
        self.__keepalive = keepalive
        self.__transport = transport
        self.__clean_start = clean_start

        self.__client_count = client_count
        self.__ip = ip
        self.__port = int(port)
        self.__protocol = protocol

class Group:
    '''
    组的对象，一个group对多个client
    '''

    @property
    def group_name(self) -> str:
        return self.__group_name

    @property
    def interval(self) -> int:
        return self.__interval

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def repeat(self) -> int:
        return self.__repeat


    @property
    def cases(self) -> list[str]:
        return self.__cases
    
    @property
    def android_setting(self) -> AndroidSetting:
        return self.__android_setting
    
    @property
    def browser_setting(self) -> BrowserSetting:
        return self.__browser_setting
    
    @property
    def desktop_setting(self) -> DesktopSetting:
        return self.__desktop_setting
    
    @property
    def http_setting(self) -> HttpSetting:
        return self.__http_setting
    
    @property
    def socket_setting(self) -> SocketSetting:
        return self.__socket_setting
    
    @property
    def mqtt_setting(self) -> MqttSetting:
        return self.__mqtt_setting

    
    def __init__(self, 
                 group_name: str,
                 cases: list[str],
                 android_setting : AndroidSetting = None,
                 browser_setting : BrowserSetting = None,
                 desktop_setting : DesktopSetting = None,
                 http_setting : HttpSetting = None,
                 socket_setting : SocketSetting = None,
                 mqtt_setting : MqttSetting = None,
                 interval: int = 1,
                 width : int = 1920, 
                 height : int = 1080,
                 debug : bool = False,
                 env : dict = {},
                 repeat : int = 1, ) -> None:
        
        

        self.__group_name = group_name
        self.__interval = interval
        self.__width = width
        self.__height = height
        self.__repeat = repeat
        self.__env = env;

        self.__cases = cases

        self.__android_setting = android_setting
        self.__browser_setting = browser_setting
        self.__desktop_setting = desktop_setting
        self.__http_setting = http_setting
        self.__socket_setting = socket_setting
        self.__mqtt_setting = mqtt_setting
        
        ## 如果是调试模式，则循环次数强制为1
        if debug:
            self.__repeat = 1
        self.__debug = debug
        

    def env(self, name : str) -> str:
        ''' 
        获取该组的内部环境变量
        Parameters
        ----------
        
        
        Returns
        -------
        str
        
        '''
        return self.__env.get(name);
        
    
