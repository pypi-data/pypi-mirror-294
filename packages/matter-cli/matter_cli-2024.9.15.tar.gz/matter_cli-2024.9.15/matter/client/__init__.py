# -*- encoding: utf-8 -*-
'''
@File		:	__init__.py
@Time		:	2024/01/05 09:50:06
@Author		:	dan
@Description:	客户端的封装，包含adb、browser、http、desktop
'''



import threading
from matter.client.adb import Adb
from matter.client.browser import Browser
from matter.client.desktop import Desktop
from matter.client.http_utils import Http
from matter.client.mqtt_utils import MqttClient
from matter.client.socket_utils import SocketClient
from matter.config import matter_config
from matter.group import AndroidSetting, Group
from matter.manager.case_manager import CaseManager
from matter.manager.proxy_manager import PROXY_MANAGER
from matter.proxy.proxy_client import ProxyClient
from matter.utils import console
import matter.utils.system_utils as system_utils


class Client:

    @property
    def proxys(self) -> list[ProxyClient]:
        return self.__proxys
    
    @property
    def adb(self) -> Adb:
        return self.__adb
    
    @property
    def browser(self) -> Browser:
        return self.__browser
    
    @property
    def desktop(self) -> Desktop:
        return self.__desktop
    
    @property
    def http(self) -> Http:
        return self.__http
    
    @property
    def socket(self) -> SocketClient:
        return self.__socket
    
    @property
    def mqtt(self) -> MqttClient:
        return self.__mqtt
    
    @property
    def client_thread(self) -> threading.Thread:
        return self.__client_thread
    
    @property
    def group_name(self) -> str:
        return self.__group_name
    
    @property
    def interval(self) -> int:
        return self.__interval
    
    @property
    def group(self) -> Group:
        return self.__group

    def __init__(self, 
                 cases: list[str],
                 adb : Adb = None, 
                 android_setting : AndroidSetting = None,
                 browser : Browser = None, 
                 desktop : Desktop = None, 
                 socket : SocketClient = None, 
                 http : Http = None, 
                 mqtt : MqttClient = None,
                 group_name : str = None,
                 group : Group = None,
                 interval : int = None, ) -> None:
        self.__adb = adb;
        self.__browser = browser;
        self.__desktop = desktop;
        self.__http = http;
        self.__socket = socket;
        self.__mqtt = mqtt;
        self.__proxys : list[str] = []
        self.__group_name = group_name
        self.__client_thread = threading.Thread(target=self.run)
        self.__started = False
        self.__case_manager = CaseManager()
        self.__cases = cases
        self.__interval = interval
        self.__group = group
        self.__android_setting = android_setting
        pass


    def append_proxy(self, server_host: str ) -> None:
        ''' 添加代理，当此Client执行某些内容时，会传递到代理服务器中，让代理执行相同内容
        
        Parameters
        ----------
        server_host : str 远端代理服务器的地址
        
        Returns
        -------
        None

        
        '''
        self.__proxys.append(server_host)
        pass


    def send_to_proxy(self, msg : str | dict) -> None:
        ''' 发送给该client对应的远程设备
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__proxys:
            return;
        for host in self.__proxys:
            PROXY_MANAGER.send_to_proxy(host, msg)
        pass


    def init_by_apk(self, apk : str, package_name : str, waiting : bool = True, uninstall : bool = False, run_app : bool = False) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        apk : str apk文件位置

        package_name : str apk文件 对应的包名

        waiting : bool = True 是否等待apk安装完成
        
        uninstall : bool = False 安装前是否卸载
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;
    
        self.adb.package_name = package_name

        if not self.adb.connected:
            self.adb.connect()
        self.adb.unlock(check_status=True)
        installed = self.adb.is_installed()
        if not installed:
            self.adb.install(apk, uninstall=uninstall)
        elif uninstall:
            self.adb.install(apk, uninstall=uninstall)

        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package == package_name:
            if not run_app:
                self.adb.app_stop(current_package)

        if self.__proxys:
            # TODO 代理处理
            pass

        return package_name


    def init_by_package(self, package_name : str, waiting : bool = True) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        apk : str apk文件位置

        package_name : str apk文件 对应的包名

        waiting : bool = True 是否等待apk安装完成
        
        uninstall : bool = False 安装前是否卸载
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;
    
        self.adb.connect()
        self.adb.package_name = package_name

        if not self.adb.is_installed(package_name):
            system_utils.exit(f'在安卓{self.adb.host}设备找不到应用{package_name}')

        self.adb.unlock(check_status=True)
        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package == package_name:
            self.adb.app_stop(current_package)
        self.adb.app_start(package_name)

        if self.__proxys:
            # TODO 代理处理
            pass

        return package_name

    def open_by_package(self, package_name : str, waiting : bool = True, restart : bool = True) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        package_name : str app 的包名
        
        waiting : bool = True 是否等待apk安装完成
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;

    
        self.adb.package_name = package_name
        if not self.adb.connected:
            self.adb.connect()

        self.adb.unlock(check_status=True)
        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package != package_name or restart:
            if current_package:
                self.adb.app_stop(current_package)
            self.adb.app_start(package_name)
            return;


    def close_by_package(self, package_name : str, waiting : bool = True) -> None:
        ''' 关闭应用
        
        Parameters
        ----------
        package_name : str app 的包名
        
        waiting : bool = True 是否等待apk安装完成
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;

    
        self.adb.package_name = package_name
        if not self.adb.connected:
            self.adb.connect()

        self.adb.unlock(check_status=True)
        self.adb.app_stop(package_name)

    def init_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.init_driver()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__init_remote_browser(self.__browser)
            pass


    def open_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.open()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__open_remote_browser(self.__browser)
            pass


    def close_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.close()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__close_remote_browser(self.__browser)
            pass

    def init_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def open_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def close_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def init_by_socket(self, waiting : bool = True) -> None:
        ''' 初始化socket
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__socket:
            return;



    def init_by_mqtt(self, waiting : bool = True) -> None:
        ''' 初始化mqtt
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__mqtt:
            return;

    def close_by_socket(self, waiting : bool = True) -> None:
        ''' 关闭socket
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__socket:
            return;


        self.__socket.close()

    def close_by_mqtt(self, waiting : bool = True) -> None:
        ''' 关闭mqtt
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__mqtt:
            return;


        self.__mqtt.close()

    def open_by_socket(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        # if not self.__socket_thread:
        #     return;

        if(self.__socket == None):
            ## 发生错误
            pass

        self.__socket.close()
        self.__socket.start()
    

    def open_by_mqtt(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        # if not self.__socket_thread:
        #     return;

        if(self.__mqtt == None):
            ## 发生错误
            pass

        lock = None;
        if waiting:
            lock = threading.Lock()

        self.__mqtt.connect(
            username=self.group.mqtt_setting.username,
            password=self.group.mqtt_setting.password,
            transport=self.group.mqtt_setting.transport,
            keepalive=self.group.mqtt_setting.keepalive,
            clean_start=self.group.mqtt_setting.clean_start,
            on_connect= lambda mqtt_client, userdata, data, code, properties : lock.release(),
        )
        lock.acquire()
        topics = self.group.mqtt_setting.subscribe_topics
        for t in topics:
            self.__mqtt.subscribe(t)

    def init_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''

        if self.__proxys:
            # TODO 代理处理
            pass


    def open_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__desktop:
            return;

        self.__desktop.open()

        if self.__proxys:
            # TODO 代理处理
            pass


    def close_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__desktop:
            return;

        self.__desktop.close()

        if self.__proxys:
            # TODO 代理处理
            pass


    def start(self) -> None:
        ''' 开始执行测试组
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        if self.__started:
            return;
        self.__started = True
        self.__client_thread.start();


    def run(self) -> None:
        ''' 线程内运行的方法
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        ## 所有测试用例执行前运行
        self.init_test_env(waiting=True)


        ## 每个测试用例重复执行的次数
        for i in range(self.group.repeat):
            for case_name in self.__cases:
                self.__before_run_case(case_name)
                try:
                    console.print_info(f"启动测试用例 - {case_name}")
                    self.__case_manager.run_case(case_name)
                    console.print_ok(f"测试通过 - {case_name}")
                except Exception as ex:
                    console.print_error(f"测试不通过 - {case_name}")
                    if matter_config.DEBUG:
                        print(ex)
                self.__after_run_case(case_name)

        self.release_test_env()

    def init_test_env(self, waiting : bool = True) -> None:
        ''' 初始化测试环境

        对于安卓，则是安装必要的apk，和启动程序

        对于desktop程序，则是打开位置的程序

        对于浏览器，则是打开浏览器并打开特定网址
        
        Parameters
        ----------
        waiting : bool 是否等待所有客户端完成
        
        Returns
        -------
        None
        
        '''
        
        if self.adb is not None:
            # TODO 增加clientid
            print("正在启动安卓测试环境")
            android_setting = self.group.android_setting
            if android_setting.android_test == 'apk':
                package_name = self.init_by_apk(android_setting.apk, 
                                waiting = waiting, 
                                uninstall=android_setting.uninstall)
                self.__package_name = package_name
            else:
                self.__package_name = android_setting.package_name
                package_name = self.init_by_package(package_name=self.__package_name, 
                                waiting = waiting)
            print("安卓测试环境启动完毕")

        if self.browser is not None:
            print("正在启动浏览器测试环境")
            self.init_by_browser(waiting=waiting)
            print("浏览器测试环境启动完毕")

        if self.http is not None:
            print("正在启动HTTP测试环境")
            self.init_by_http(waiting=waiting)
            print("HTTP测试环境启动完毕")

        if self.desktop is not None:
            print("正在启动桌面程序测试环境")
            self.init_by_desktop(waiting=waiting)
            print("桌面程序测试环境启动完毕")

        if self.socket is not None:
            print("正在启动Socket测试环境")
            self.init_by_socket(waiting=waiting)
            print("Socket测试环境启动完毕")

        if self.mqtt is not None:
            print("正在启动Mqtt测试环境")
            self.init_by_mqtt(waiting=waiting)
            print("Mqtt测试环境启动完毕")


    def __before_run_case(self, case_name:str ) ->  None:
        ''' 
        在执行测试用例前执行
        '''
        if self.adb:
            self.open_by_package(package_name=self.__package_name, 
                                    restart=self.group.android_setting.restart)

        if self.browser:
            self.open_by_browser()

        if self.http:
            self.open_by_http()

        if self.desktop:
            self.open_by_desktop()

        if self.socket:
            self.open_by_socket()

        if self.mqtt:
            self.open_by_mqtt()


    def release_test_env(self) -> None:
        '''  释放测试环境
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if self.adb is not None:
            self.close_by_package(package_name=self.__package_name,  waiting=True)

        if self.browser is not None:
            self.close_by_browser(waiting=True)

        if self.http is not None:
            self.close_by_http(waiting=True)

        if self.desktop is not None:
            self.close_by_desktop(waiting=True)

        if self.socket is not None:
            self.close_by_socket(waiting=True)

        if self.mqtt is not None:
            self.close_by_mqtt(waiting=True)


    def __after_run_case(self, case_name:str) ->  None:
        ''' 
        在执行测试用例前执行
        '''
        pass