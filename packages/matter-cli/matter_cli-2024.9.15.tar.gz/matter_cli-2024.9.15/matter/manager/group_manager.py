# -*- encoding: utf-8 -*-
'''
@File		:	group_manager.py
@Time		:	2024/01/05 09:58:34
@Author		:	dan
@Description:	关于组的管理器
'''

from matter.client import Client
from matter.client.adb import Adb
from matter.client.browser import Browser
from matter.client.desktop import Desktop
from matter.client.http_utils import Http
from matter.client.mqtt_utils import MqttClient
from matter.client.mumu import MuMonitor
from matter.client.socket_utils import SocketClient
from matter.config import matter_config
from matter.group import AndroidSetting, BrowserSetting, DesktopSetting, Group, HttpSetting, MqttSetting, SocketSetting
from matter.manager.case_manager import CaseManager
from matter.manager.proxy_manager import PROXY_MANAGER
from matter.utils.singleton import singleton
import matter.utils.system_utils as system_utils
import os
import yaml
import threading
import time


BROWSER_ENGINES = ['chrome', 'edge', 'firefox', 'explorer', 'safari']

@singleton
class GroupManager:
    '''
    关于组的管理器
    '''

    @property
    def groups(self) -> dict[str, Group]:
        return self.__groups
    
    @property
    def is_inited(self) -> bool:
        """
        是否初始化
        """
        return self.__is_inited
    
    @property
    def yml_path(self) -> str:
        """
        yml文件位置
        """
        return self.__yml_path
    
    
    def current_group(self) -> Group:
        ''' 获取当前Client对应的组
        
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        current_thread = threading.current_thread()
        client : Client = self.clients_by_thread[current_thread.name]
        group_name = client.group_name
        return self.groups[group_name]
    
    def current_client(self) -> Client:
        ''' 获取当前Client
        
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        current_thread = threading.current_thread()
        client : Client = self.clients_by_thread[current_thread.name]
        return client
    
    @property
    def clients_by_thread(self) -> dict[str, Client]:
        return self.__clients_by_thread
    
    @property
    def debug(self) -> bool:
        '''
        当前是否为调试模式
        '''
        return self.__debug
    

    def __init__(self) -> None:
        self.__is_inited = False
        self.__groups : dict[str, Group] = dict()
        self.__clients_by_thread : dict[str, Client] = dict()
        self.__clients : list[Client] = []
        self.__mumu_monitors : list[MuMonitor] = []
        self.__case_manager = CaseManager()
        pass


    def init(self, yml_path: str = "./matter.yml") -> None:
        ''' 
        Parameters
        ----------
        yml_path: str yml文件目录
        
        Returns
        -------
        None
        
        '''
        self.__is_inited = True
        self.__yml_path = yml_path
        if not os.path.isfile(yml_path):
            system_utils.exit(f'找不到{yml_path}')
        with open(self.yml_path, 'r', encoding='utf-8') as f:
            result : dict = yaml.load(f.read(), Loader=yaml.FullLoader)

        version = result.get("version");
        if version == None:
            system_utils.exit(f'yml中的version必填')
        self.__debug = result.get('debug')
        if self.__debug is None: self.__debug = False
        matter_config.DEBUG = self.__debug

        ## TODO 未来此处可能会根据版本号读取yml内容
        matter_dict : dict = result.get('matter')
        if matter_dict is None:
            system_utils.exit(f'yml中的matter必填')
        for i in range(len(matter_dict)):
            for group_name in matter_dict.keys():
                print(f"正在初始化 {group_name}")
                group_dict : dict = matter_dict.get(group_name)

                cases = group_dict.get('cases')
                if not cases:
                    system_utils.exit(f'{group_name}的cases参数必填')
                for case_name in cases:
                    test_case = self.__case_manager.find_case(case_name)
                    if not test_case:
                        system_utils.exit(f'不存在测试用例 {test_case}')

                width = 1920 if group_dict.get('width') is None else group_dict.get('width')
                self.check_type(width, int, "width 必须是整数，且大于0")

                height = 1080 if group_dict.get('height') is None else group_dict.get('height') 
                self.check_type(height, int, "height 必须是整数，且大于0")

                interval = 1 if group_dict.get('interval') is None else group_dict.get('interval')
                self.check_type(interval, int, "interval 必须是整数，且大于0")

                repeat = 1 if group_dict.get('repeat') is None else group_dict.get('repeat')
                self.check_type(repeat, int, "repeat 必须是整数，且大于0")

                env_list = [] if group_dict.get('env') is None else group_dict.get('env')
                self.check_type(env_list, list, "env 是一个数组")
                env = {}
                for item in env_list:
                    self.check_type(item, str, "env 必须是一个数组，而且每项格式为 xxx=yyy")
                    item : str = item
                    if not item.__contains__("="):
                        system_utils.exit("env 必须是一个数组，而且每项格式为 xxx=yyy")
                    key = item[0 : item.index("=")]
                    value = item[item.index("=") + 1 : len(item)]
                    env[key] = value;


                self.__clients = []
                android_setting = self.analys_android_setting(group_dict.get('android'))
                browser_setting = self.analys_browser_setting(group_dict.get('browser'))
                desktop_setting = self.analys_desktop_setting(group_dict.get('desktop'))
                http_setting = self.analys_http_setting(group_dict.get('http'))
                socket_setting = self.analys_socket_setting(group_dict.get('socket'))
                mqtt_setting = self.analys_mqtt_setting(group_dict.get('mqtt'))

                group = Group(group_name=group_name, 
                              android_setting=android_setting,
                              browser_setting=browser_setting,
                              desktop_setting=desktop_setting,
                              mqtt_setting=mqtt_setting,
                              http_setting=http_setting,
                              socket_setting=socket_setting,
                              debug=self.__debug,
                              cases=cases,
                              env=env,
                              interval=interval, 
                              width=width, height=height, repeat=repeat)
                

                if mqtt_setting is not None:
                    self.__clients.extend(self.analys_clients_mqtt(mqtt_setting, group))
                if socket_setting is not None:
                    self.__clients.extend(self.analys_clients_socket(socket_setting, group))
                if http_setting is not None:
                    self.__clients.extend(self.analys_clients_http(http_setting, group))
                if desktop_setting is not None:
                    self.__clients.extend(self.analys_clients_desktop(desktop_setting, group))
                if browser_setting is not None:
                    self.__clients.extend(self.analys_clients_browser(browser_setting, group))
                if android_setting is not None:
                    self.__clients.extend(self.analys_clients_android(android_setting, group))

                self.__groups[group_name] = group

                if len(self.__clients) == 0:
                    system_utils.exit(f'请在{group_name}中定义客户端信息，可以是android、browser、desktop、http、socket、mqtt 其中一项')

                for client in self.__clients:
                    self.clients_by_thread[client.client_thread.name] = client

                print(f"初始化 {group_name} 完毕")

        if not self.__groups:
            system_utils.exit('请在matter.yml中定义组信息')
            
        ## 连接到远程的代理服务器
        if not self.__debug:
            PROXY_MANAGER.connect_to_proxy(waiting = True)

        ## 如果是调试模式，则循环次数强制为1
        if self.__debug:
            print("注意！你正在运行在Debug模式下，该模式仅适用于开发环境，在正式测试环境中请去除Debug模式！")

        # ## 等待所有客户端完成初始化
        # self.init_test_env(waiting = True)

    def analys_clients_android(self, android_setting : AndroidSetting, group : Group):
        clients = []
        apk = android_setting.apk
        package_name = android_setting.package_name
        if apk is None and package_name is None:
            system_utils.exit('apk和package_name必须填一个！')

        android_test = "apk" if package_name is None else "package_name"
        uninstall = android_setting.uninstall
        restart = android_setting.restart

        ## 开启的mumu模拟器
        targets = android_setting.targets
        mumu = android_setting.mumu
        if mumu:
            if not targets:
                targets = []
            print("正在启动mumu模拟器")
            self.__mumu_monitors : list[MuMonitor] = []
            for i in range(mumu):
                m = MuMonitor(index = i)
                m.start()
                self.__mumu_monitors.append(m)

            ## 等待模拟器启动完毕
            not_ready = True
            while not_ready:
                all_ok = True
                for monitor in self.__mumu_monitors:
                    if(monitor.player_state == MuMonitor.NOT_RUNNING or monitor.player_state == MuMonitor.STARTING):
                        monitor.refresh_state()
                        all_ok = False

                if all_ok:
                    not_ready = False
                else:
                    time.sleep(1)

            print("启动mumu模拟器完毕")
            for monitor in self.__mumu_monitors:
                adb_host = monitor.refresh_adb_host()
                targets.append(adb_host)


        # time.sleep(3)

        if targets is not None:
            for t in targets:
                if type(t) != str:
                    system_utils.exit('android 下的targets必须是字符串列表！')
                    return;
                self.check_adb_format(t)
                client = Client(adb = Adb(t), 
                                group_name = group.group_name, 
                                cases=group.cases, 
                                interval=group.interval, 
                                group=group,
                                android_setting=android_setting)
                clients.append(client)
        return clients






    def analys_clients_browser(self, browser_setting : BrowserSetting, group : Group):
        clients = []

        root_url = browser_setting.url
        if root_url == None:
            system_utils.exit('browser 下的url 必填！')
        if type(root_url) != str:
            system_utils.exit('browser 下的url 必须为字符串！')

        client_count = browser_setting.client_count
        ## 窗口大小
        window_size = browser_setting.window_size
        window_size = window_size

        ## selenium 浏览器参数
        arguments = browser_setting.arguments


        targets = browser_setting.targets
        if targets is not None:
            for j in range(client_count):
                for t in targets:
                    if type(t) != str:
                        system_utils.exit('browser 下的targets必须是字符串列表！')
                        return;
                    self.check_browser_target(t)
                    client = Client(browser = Browser(engine=t, url=root_url, window_size=window_size, arguments=arguments), 
                                    group_name = group.group_name, 
                                    group=group,
                                    cases=group.cases, 
                                    interval=group.interval)
                    
                    # TODO 这里代理设置有问题，后续再优化
                    # if browser_setting.remote_proxys is not None:
                    #     remote_proxys = browser_setting.remote_proxys
                    #     for proxy in remote_proxys:
                    #         self.check_proxy_format(proxy)
                    #         client.append_proxy(proxy)
                    #         PROXY_MANAGER.append_proxy(proxy)
                    clients.append(client)
        return clients

    def analys_clients_desktop(self, desktop_setting : DesktopSetting, group : Group):
        clients = []

        bin = desktop_setting.bin
        if bin is None:
            system_utils.exit('desktop 下的bin为必填且必须是字符串列表！')
        ## 是否每次测试都重新启动
        restart = desktop_setting.restart
        ## 窗口大小
        window_size = desktop_setting.window_size
    
        if not os.path.exists(bin):
            system_utils.exit(f'找不到 {bin}, 请确认该文件真实存在')
        client = Client(desktop = Desktop(bin, window_size = window_size), 
                        group_name = group.group_name, 
                        group=group,
                        cases=group.cases, interval=group.interval)
        
        # TODO 这里代理设置有问题，后续再优化
        # if desktop_setting.remote_proxys is not None:
        #     remote_proxys = desktop_setting.remote_proxys
        #     for proxy in remote_proxys:
        #         self.check_proxy_format(proxy)
        #         client.append_proxy(proxy)
        #         PROXY_MANAGER.append_proxy(proxy)
        clients.append(client)
        return clients

    def analys_clients_http(self, http_setting : HttpSetting, group : Group):
        clients = []
        client_count = http_setting.client_count
        host = http_setting.host
        for i in range(client_count):
            clients.append(Client(http = Http(host), 
                group=group,
                group_name = group.group_name, 
                cases=group.cases))
        return clients

    def analys_clients_socket(self, socket_setting : SocketSetting, group : Group):
        clients = []
        client_count = socket_setting.client_count
        
        for i in range(client_count):
            clients.append(Client(socket = SocketClient(
                    protocol=socket_setting.protocol, 
                    server_host=socket_setting.ip, 
                    server_port=socket_setting.port), 
                group=group,
                group_name = group.group_name, 
                cases=group.cases, interval=group.interval))

        return clients

    def analys_clients_mqtt(self, mqtt_setting : MqttSetting, group : Group):
        clients = []
        
        for i in range(mqtt_setting.client_count):
            clients.append(Client(
                mqtt = MqttClient(
                    protocol=mqtt_setting.protocol, 
                    server_host=mqtt_setting.ip,
                    server_port=mqtt_setting.port), 
                group=group,
                group_name = group.group_name, 
                cases=group.cases, 
                interval=group.interval))

        return clients


    def append(self, group: Group):
        """
        新增组
        """
        self.groups.append(group)
        pass

    def check_browser_target(self, engine : str):
        ''' 检查浏览器引擎是否正确，浏览器引擎使用的selenium的实现
        
        Parameters
        ----------
        engine : engine 浏览器引擎
        
        Returns
        -------
        None
        
        '''
        version = None
        if engine.__contains__("@"):
            arr = engine.split("@")
            engine = arr[0]
            version = arr[1]
        engine = engine.lower()
        if BROWSER_ENGINES.__contains__(engine):
            return;
        system_utils.exit(f'browser 下的 targets 内的 {engine} 不支持，必须为 {", ".join(BROWSER_ENGINES)} 中的一个 ！')




    def check_adb_format(self, url : str) -> None:
        ''' 检查adb的路径是否正确，必须为 IP、IP:PORT 或 local 关键词
        
        Parameters
        ----------
        url : str adb设备的路径
        
        Returns
        -------
        None
        
        '''
        if url == 'local':
            return;
        if url.__contains__(":"):
            arr = url.split(":")
            ip = arr[0]
            port = arr[1]
            if not system_utils.isIP(ip):
                system_utils.exit(f'android 下的 targets 内的 {url} 格式不正确，必须为 IP、IP:PORT 或 local 关键词 ！')
            if not system_utils.isPort(port):
                system_utils.exit(f'android 下的 targets 内的 {url} 格式不正确，必须为 IP、IP:PORT 或 local 关键词 ！')
        else:
            if not system_utils.isIP(url):
                system_utils.exit(f'android 下的 targets 内的 {url} 格式不正确，必须为 IP、IP:PORT 或 local 关键词 ！')
        pass



    def check_proxy_format(self, url : str) -> None:
        ''' 检查remote_proxys的路径是否正确，必须为 IP、IP:PORT 或 local 关键词
        
        Parameters
        ----------
        url : str adb设备的路径
        
        Returns
        -------
        None
        
        '''
        if url.__contains__(":"):
            arr = url.split(":")
            ip = arr[0]
            port = arr[1]
            if not system_utils.isIP(ip):
                system_utils.exit(f'remote_proxys 内的 {url} 格式不正确，必须为 IP、IP:PORT ！')
            if not system_utils.isPort(port):
                system_utils.exit(f'remote_proxys 内的 {url} 格式不正确，必须为 IP、IP:PORT ！')
        else:
            if not system_utils.isIP(url):
                system_utils.exit(f'remote_proxys 内的 {url} 格式不正确，必须为 IP、IP:PORT ！')
        pass


    


    def check_host_format(self, url : str) -> None:
        ''' 检查http的路径是否正确，必须为 http://IP、http://IP:PORT、https://IP、https://IP:PORT 
        
        Parameters
        ----------
        url : str adb设备的路径
        
        Returns
        -------
        None
        
        '''
        if not url.startswith('http'):
            system_utils.exit(f'http 下的 host 内的 {url} 格式不正确，必须为 http://IP、http://IP:PORT、https://IP、https://IP:PORT ！')

        if url.startswith("https://"):
            ip_port = url[8:]
        elif url.startswith("http://"):
            ip_port = url[7:]
        else:
            system_utils.exit(f'http 下的 host 内的 {url} 格式不正确，必须为 http://IP、http://IP:PORT、https://IP、https://IP:PORT ！')

        if ip_port.__contains__(":"):
            arr = ip_port.split(":")
            ip = arr[0]
            port = arr[1]
            if not system_utils.isIP(ip):
                system_utils.exit(f'http 下的 host 内的 {url} 格式不正确，必须为 http://IP、http://IP:PORT、https://IP、https://IP:PORT ！')
            if not system_utils.isPort(port):
                system_utils.exit(f'http 下的 host 内的 {url} 格式不正确，必须为 http://IP、http://IP:PORT、https://IP、https://IP:PORT ！')
        else:
            if not system_utils.isIP(ip_port):
                system_utils.exit(f'android 下的 targets 内的 {url} 格式不正确，必须为 IP、IP:PORT 或 local 关键词 ！')
        pass


    def check_socket_format(self, url : str) -> None:
        ''' 检查http的路径是否正确，必须为 udp://IP:PORT，tcp://IP:PORT 
        
        Parameters
        ----------
        url : str adb设备的路径
        
        Returns
        -------
        None
        
        '''
        if not url.startswith('tcp') and not url.startswith('udp'):
            system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')

        if url.startswith("udp://"):
            ip_port = url[6:]
        elif url.startswith("tcp://"):
            ip_port = url[6:]
        else:
            system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')

        if ip_port.__contains__(":"):
            arr = ip_port.split(":")
            ip = arr[0]
            port = arr[1]
            if not system_utils.isIP(ip):
                system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
            if not system_utils.isPort(port):
                system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        else:
            system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        pass



    def check_mqtt_format(self, url : str) -> None:
        ''' 检查http的路径是否正确，必须为 mqtt://IP:PORT，mqtts://IP:PORT 
        
        Parameters
        ----------
        url : str adb设备的路径
        
        Returns
        -------
        None
        
        '''
        if not url.startswith('mqtt') and not url.startswith('mqtts'):
            system_utils.exit(f'socket 下的 host 内的 {url} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')

        if url.startswith("mqtt://"):
            ip_port = url[7:]
        elif url.startswith("mqtts://"):
            ip_port = url[8:]
        else:
            system_utils.exit(f'mqtt 下的 host 内的 {url} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')

        if ip_port.__contains__(":"):
            arr = ip_port.split(":")
            ip = arr[0]
            port = arr[1]
            if not system_utils.isIP(ip):
                system_utils.exit(f'mqtt 下的 host 内的 {url} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
            if not system_utils.isPort(port):
                system_utils.exit(f'mqtt 下的 host 内的 {url} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        else:
            system_utils.exit(f'mqtt 下的 host 内的 {url} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        pass


    def check_type(self, value : any, t : type, error_message: str) -> None:
        ''' 检查格式是否正确
        
        Parameters
        ----------
        value : any 要判断的值

        t : type 目标类型

        error_message : type 不匹配时提示错误
        
        Returns
        -------
        None
        
        '''
        if type(value) != t:
            system_utils.exit(error_message)
        pass


    def start(self) -> None:
        ''' 执行测试
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        for client in self.__clients:
            client.start()



    def analys_android_setting(self, android : dict) -> AndroidSetting:
        ''' 解析yml文件，获取安卓的设置
        
        Parameters
        ----------
        
        
        Returns
        -------
        AndroidSetting
        
        '''
        if not android:
            return None;

        apk = android.get('apk')
        package_name = android.get('package_name')
        if apk is None and package_name is None:
            system_utils.exit('apk和package_name必须填一个！')
        android_test = "apk" if package_name is None else "package_name"
        uninstall = False if android.get('uninstall') is None else android.get('uninstall')
        restart = True if android.get('restart') is None else android.get('restart')
        mumu = 0 if android.get('mumu') is None else android.get('mumu')
        self.check_type(mumu, int, "mumu 必须是一个数字，而且大于等于0")
        if mumu < 0:
            system_utils.exit("mumu 必须是一个数字，而且大于等于0")
        targets = ['local'] if android.get('targets') is None else android.get('targets')
        self.check_type(targets, list, "targets 是一个字符串数组，可以取值 local，或 IP:PORT，其中IP:PORT 是 adb远程监听地址和端口")
        for t in targets:
            if not t.__contains__(':'):
                if t == 'local':
                    continue
                if system_utils.isIP(t):
                    continue
            else:
                arr = t.split(':')
                if len(arr) == 2:
                    ip, port = arr
                    if system_utils.isIP(ip) and system_utils.isPort(port):
                        continue;
            system_utils.exit("targets 是一个字符串数组，可以取值 'local'，或 IP:PORT 或 IP，其中 IP:PORT 是 adb远程监听地址和端口")
        
        

        restart = True if android.get('restart') is None else android.get('restart')
        return AndroidSetting(
            apk=apk, 
            package_name=package_name, 
            uninstall=uninstall, 
            mumu=mumu, 
            targets=targets, 
            restart=restart, 
            android_test=android_test)


    def analys_browser_setting(self, browser : dict) -> BrowserSetting:
        ''' 获取浏览器参数设置
        
        Parameters
        ----------
        
        
        Returns
        -------
        BrowserSetting
        
        '''
        if browser is None:
            return None;
        root_url = None if browser.get('url') is None else browser.get('url')
        if root_url == None:
            system_utils.exit('browser 下的url 必填！')
        if type(root_url) != str:
            system_utils.exit('browser 下的url 必须为字符串！')

        client_count = 1 if browser.get('client_count') is None else browser.get('client_count')
        ## 窗口大小
        window_size = 'max' if browser.get('window_size') is None else browser.get('window_size')
        window_size = window_size

        ## selenium 浏览器参数
        arguments = [] if browser.get('arguments') is None else browser.get('arguments')
        self.check_type(arguments, list, "arguments 必须是一个数组")

        targets = None if browser.get('targets') is None else browser.get('targets')
        self.check_type(targets, list, "targets 必须是一个数组")
        eng = Browser.ENGINES.keys()
        for t in targets:
            if eng.__contains__(t):
                continue
            engins = '\\'.join(Browser.ENGINES.keys())
            system_utils.exit(f"browser 下 targets 的取值范围为 {engins}")

        return BrowserSetting(
            url=root_url, 
            window_size=window_size, 
            client_count=client_count,
            targets=targets,
            arguments=arguments)
    

    

    def analys_http_setting(self, http : dict) -> HttpSetting:
        ''' 获取Http请求参数设置
        
        Parameters
        ----------
        
        
        Returns
        -------
        HttpSetting
        
        '''
        if http is None:
            return None;
        host = http.get('host')
        self.check_type(host, str, f'host 下的 host 内的 {host} 格式不正确，必须为 http://IP(HOST):PORT 或 https://IP(HOST):PORT  ！');
        self.check_host_format(host)
        arr = host.split(":")
        if len(arr) < 3:
            system_utils.exit(f'host 下的 host 内的 {host} 格式不正确，必须为 http://IP(HOST):PORT 或 https://IP(HOST):PORT  ！')
        protocol = arr[0]
        ip = arr[1]
        ip = ip[2:]
        port = arr[2]
        
        client_count = 1 if http.get('client_count') is None else http.get('client_count')
        self.check_type(client_count, int, 'client_count 必须是一个数字，而且大于等于0');
        return HttpSetting(host=host, client_count=client_count)
    

    

    def analys_socket_setting(self, socket : dict) -> SocketSetting:
        ''' 获取Socket参数设置
        
        Parameters
        ----------
        
        Returns
        -------
        SocketSetting
        
        '''
        if socket is None:
            return None;
        host = socket.get('host')
        self.check_type(host, str, f'socket 下的 host 内的 {host} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！');

        client_count = 1 if socket.get('client_count') is None else socket.get('client_count')
        self.check_type(client_count, int, 'client_count 必须是一个数字，而且大于等于0');

        self.check_socket_format(host)
        arr = host.split(":")
        if len(arr) < 3:
            system_utils.exit(f'socket 下的 host 内的 {host} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        protocol = arr[0]
        ip = arr[1]
        ip = ip[2:]
        port = arr[2]
        if not system_utils.isIP(ip):
            system_utils.exit(f'socket 下的 host 内的 {host} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        if not system_utils.isPort(port):
            system_utils.exit(f'socket 下的 host 内的 {host} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        if protocol != 'tcp' and protocol != 'udp':
            system_utils.exit(f'socket 下的 host 内的 {host} 格式不正确，必须为 udp://IP:PORT 或 tcp://IP:PORT  ！')
        port = int(port)
        return SocketSetting(host=host, protocol=protocol, ip=ip, port=port, client_count=client_count)
    

    

    def analys_mqtt_setting(self, mqtt : dict) -> SocketSetting:
        ''' 获取Mqtt参数设置
        
        Parameters
        ----------
        
        Returns
        -------
        SocketSetting
        
        '''
        if mqtt is None:
            return None;
    
        client_count = 1 if mqtt.get('client_count') is None else mqtt.get('client_count')
        host : str = mqtt.get('host')
        self.check_mqtt_format(host)
        arr = host.split(":")
        if len(arr) < 3:
            system_utils.exit(f'mqtt 下的 host 内的 {host} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        protocol = arr[0]
        ip = arr[1]
        ip = ip[2:]
        port = arr[2]
        if not system_utils.isIP(ip):
            system_utils.exit(f'mqtt 下的 host 内的 {host} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        if not system_utils.isPort(port):
            system_utils.exit(f'mqtt 下的 host 内的 {host} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        if protocol != 'mqtt' and protocol != 'mqtts':
            system_utils.exit(f'mqtt 下的 host 内的 {host} 格式不正确，必须为 mqtt://IP:PORT 或 mqtts://IP:PORT  ！')
        port = int(port)

        host = mqtt.get('host')
        username = None if mqtt.get('username') is None else mqtt.get('username')
        password = None if mqtt.get('password') is None else mqtt.get('password')
        transport = 'tcp' if mqtt.get('transport') is None else mqtt.get('transport')

        keepalive = 60 if mqtt.get('keepalive') is None else mqtt.get('keepalive')
        clean_start = True if mqtt.get('clean_start') is None else mqtt.get('clean_start')
        subscribe_topics = [] if mqtt.get('subscribe_topics') is None else mqtt.get('subscribe_topics')
        self.check_type(transport, str, "transport 必须是字符串，且只能取值 tcp、websocket")
        if transport != 'tcp' and transport != 'websocket':
            system_utils.exit("transport 必须是字符串，且只能取值 tcp、websocket")
        self.check_type(keepalive, int, "keepalive 必须是整数，且大于0")
        self.check_type(clean_start, bool, "clean_start 只能取值 true 或者 false")
        self.check_type(subscribe_topics, list, "subscribe_topics 必须是字符串列表")
        self.check_type(subscribe_topics, list, "subscribe_topics 必须是字符串列表")
        for t in subscribe_topics:
            self.check_type(t, str, "subscribe_topics 必须是字符串列表")


        return MqttSetting(host=host, 
                           client_count=client_count,
                           ip=ip,
                           port=port,
                           protocol=protocol,
                           username=username, 
                           password=password, 
                           transport=transport, 
                           keepalive=keepalive, 
                           subscribe_topics=subscribe_topics, 
                           clean_start=clean_start)
    

    

    def analys_desktop_setting(self, desktop : dict) -> DesktopSetting:
        ''' 获取桌面程序参数设置
        
        Parameters
        ----------
        
        Returns
        -------
        DesktopSetting
        
        '''
        if desktop is None:
            return None;

        bin = desktop.get('bin')
        if bin is None:
            system_utils.exit('desktop 下的bin为必填且必须是字符串列表！')
        ## 是否每次测试都重新启动
        restart = True if desktop.get('restart') is None else desktop.get('restart')
        ## 窗口大小
        window_size = 'max' if desktop.get('window_size') is None else desktop.get('window_size')
        if not os.path.exists(bin):
                system_utils.exit(f'找不到 {bin}, 请确认该文件真实存在')

        
        return DesktopSetting(bin=bin, restart=restart, window_size=window_size)

GROUP_MANAGER = GroupManager()

