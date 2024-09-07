# -*- encoding: utf-8 -*-
'''
@File		:	adb.py
@Time		:	2024/01/05 09:46:16
@Author		:	dan
@Description:   使用了adbutils作为技术实现，详情查看 https://github.com/openatx/adbutils
'''
import sys
if __name__ == '__main__':
    sys.path.append(".")

import random
import adbutils
import xml.dom.minidom
from xml.dom.minidom import Element
import time
from matter.utils.command import cmd, cmd_with_content
from matter.utils.console import print_error, print_info, print_ok, print_warning
from apkfile import ApkFile


class Rect:
    @property
    def x0(self) -> float:
        return self.__x0
    
    @x0.setter
    def x0(self, value : float):
        self.__x0 = value

    @property
    def y0(self) -> float:
        return self.__y0
    
    @y0.setter
    def y0(self, value : float):
        self.__y0 = value

    @property
    def x1(self) -> float:
        return self.__x1
    
    @x1.setter
    def x1(self, value : float):
        self.__x1 = value

    @property
    def y1(self) -> float:
        return self.__y1
    
    @y1.setter
    def y1(self, value : float):
        self.__y1 = value

    def __init__(self, x0 = None, y0 = None, x1 = None, y1 = None) -> None:
        self.__x0 = x0
        self.__x1 = x1
        self.__y0 = y0
        self.__y1 = y1

class AdbElement:
    """
    <node index="1" 
        text="上滑解锁"
        resource-id="com.android.systemui:id/hw_keyguard_indication_text"
        class="android.widget.TextView" package="com.android.systemui"
        content-desc="" 
        checkable="false" 
        checked="false" 
        clickable="false"
        enabled="true" 
        focusable="false" 
        focused="false" 
        scrollable="false"
        long-clickable="false" 
        password="false" 
        selected="false"
        bounds="[486,177][654,234]" />
    """

    @property
    def bound(self) -> Rect:
        return self.__bound
    
    @bound.setter
    def bound(self, value : Rect):
        self.__bound = value


# TODO ADB 所有方法改成同步方法
class Adb:
    ''' 
    adb 连接封装
    '''


    adb_server = None
    

    @property
    def connected(self) -> bool:
        ''' 
        是否已连接
        '''
        return self.__connected

    @property
    def device(self) -> adbutils.AdbClient:
        return self.__device
    
    @property
    def package_name(self) -> str:
        return self.__package_name
    
    @package_name.setter
    def package_name(self, value : str):
        self.__package_name = value

    @property
    def host(self) -> str:
        '''
        设备的位置
        '''
        if self.__ip == 'local':
            return 'local'
        
        return f'{self.__ip}:{self.__port}'
    
    def __init__(self, seril: str = 'local', package_name : str = None) -> None:
        self.__connected = False
        self.__device = None
        self.__package_name = package_name
        if not Adb.adb_server:
            Adb.adb_server = adbutils.AdbClient(socket_timeout=9.)
        if seril == 'local':
            self.__ip = 'local'
            # self.__device = self.__adb_server.device(transport_id=0)
            return
        else:
            mic = seril.index(":")
            port = 5555
            if mic != -1:
                port = int(seril[mic + 1 :])
                ip = seril[0 : mic]
            else:
                ip = seril
            self.__ip = ip
            self.__port = port
            # self.__device = self.__adb_server.device(self.__ip + ":" + self.__port.__str__())
        pass


    def connect(self) -> bool:
        ''' 连接到安卓设备
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool 连接成功与失败
        
        '''
        if self.connected:
            return True
        if not self.__device:
            if self.__ip == 'local':
                self.__ip = 'local'
                self.__device = Adb.adb_server.device(transport_id=0)
                self.__connected = True
                return
            else:
                host = self.__ip + ":" + self.__port.__str__()
                self.check_adb_connected(host)
                self.__device = Adb.adb_server.device(host)
                self.__connected = True
            pass
            return True
        return False
    

    def check_adb_connected(self, host) -> bool:
        ''' 
        防止重复调用adb connect
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        all_connected = cmd_with_content('adb', ['devices']).split('\n')
        all_connected = all_connected[1:]
        for line in all_connected:
            if len(line) == 0:
                continue;
            target, state = line.split('\t')
            if host == target and state == 'device':
                return True
        cmd('adb', ['connect', host])
        
        pass

    def touch(self, x : int | float, y: int | float) -> bool:
        ''' 模拟点击
        
        Parameters
        ----------
        x : int | float, 点击位置
        
        y: int | float, 点击位置
        
        
        Returns
        -------
        bool
        
        '''
        if not self.__connected:
            self.connect()

        self.__device.click(x, y)
        return True
    

    def monkey(self, duration : int = 100, times : int = 10000) -> bool:
        ''' 进入monkey测试
        
        参考 https://blog.csdn.net/fenglolo/article/details/108894278

        Parameters
        ----------
        duration : int = 500 每次操作间隔
        
        times : int = 1000 操作次数
        
        Returns
        -------
        bool
        
        '''
        if not self.__connected:
            self.connect()

        self.__device.shell(f"monkey -p {self.__package_name} -v -v --throttle {duration} {times}")
        return True


    
    

    def is_installed(self, package_name):
        ''' 
        是否安装了某包名
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        if not self.__connected:
            self.connect()
        packages = self.__device.shell('pm list packages').splitlines()
        return packages.__contains__(f'package:{package_name}')


    def install(self, apk_path : str, uninstall: bool = False) -> bool:
        ''' 安装应用
        
        Parameters
        ----------
        apk_path : str apk的位置，可以是本地路径，也可以是http路径

        uninstall : bool 是否卸载原应用
        
        Returns
        -------
        bool
        
        '''
        if not self.__connected:
            self.connect()

        self.__device.install(path_or_url=apk_path, uninstall=uninstall)
        return True
    
    
    def get_apk_info(self, apk_path: str):
        ''' 
        获取apk信息
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        apk_file = ApkFile(path=apk_path)
        return {
            "package_name": apk_file.package_name,
            "version_name": apk_file.version_name,
            "version_code": apk_file.version_code,
            "min_sdk_version": apk_file.min_sdk_version,
            "target_sdk_version": apk_file.target_sdk_version,
        }

    def slide(self, begin : tuple | list, end : tuple | list, speed : float | int = 1):
        """ 模拟滑动

        Parameters
        ----------
        begin : tuple | list
            起始点坐标，格式为 [x, y]

        end : tuple | list
            结束点坐标，格式为 [x, y]

        speed : float | int
            滑动经过的时间

        Returns
        -------
        bool
            执行成功 True
            执行失败 False
        """
        if not self.__connected:
            self.connect()

        self.__device.swipe(begin[0], begin[1], end[0], end[1], duration=speed)
        return True
    

    def touch_element(self, element : dict) -> bool:
        ''' 根据元素点击
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not element:
            print_error('点击的元素为空')
            return False
        if not self.__connected:
            self.connect()
        x1, y1, x2, y2 = element['bounds']
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        touch_x = random.randrange(start=x1, stop=x2, step=1)
        touch_y = random.randrange(start=y1, stop=y2, step=1)
        try:
            self.touch(touch_x, touch_y)
        except:
            print_error(f"点击的元素发生异常，元素的属性为 {element}")
    

    def find_element(self, by: str, value : str):
        """ 查找元素

        Parameters
        ----------
        by: str 通过什么查找
        
        value : str 相应的值

        Returns
        -------
        """
        from lxml import etree

        if not self.__connected:
            self.connect()

        xml_str = self.__device.dump_hierarchy()

        supermarket = etree.fromstring(xml_str.encode('utf-8'))
        if by == 'text':
            node = supermarket.xpath(f'//node[@text="{value}"]')
        if by == 'id':
            node = supermarket.xpath(f'//node[@resource-id="{self.__package_name}:id/{value}"]')
        if by == 'content':
            node = supermarket.xpath(f'//node[@content-desc="{value}"]')
        if by == 'xpath':
            node = supermarket.xpath(value)

        if type(node) == list:
            if len(node) == 0:
                return None;
            node = node[0]
        if node is None:
            print_warning(f"根据以下条件查找不到元素 [by={by}, value={value}]")
            return None;
        """
        <node index="1" 
            text="上滑解锁"
            resource-id="com.android.systemui:id/hw_keyguard_indication_text"
            class="android.widget.TextView" package="com.android.systemui"
            content-desc="" 
            checkable="false" 
            checked="false" 
            clickable="false"
            enabled="true" 
            focusable="false" 
            focused="false" 
            scrollable="false"
            long-clickable="false" 
            password="false" 
            selected="false"
            bounds="[486,177][654,234]" />
        """
        node_dict = {}
        for key in node.attrib.keys():
            value = node.attrib.get(key)
            if key == 'bounds':
                value = value[1 : len(value) - 1]
                lt, br = value.split("][")
                # lt = lt[0 : len(lt)]
                # br = br[0 : len(br)]
                x0, y0 = lt.split(",")
                x1, y1 = br.split(",")
                x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
                value = [x0, y0, x1, y1]
            node_dict[key] = value
            
        return node_dict
    

    def window_size(self) -> tuple:
        ''' 窗口大小
        
        Parameters
        ----------
        
        
        Return
        ----------
        tuple 例如 (1000, 1920)
        '''
        return self.__device.window_size();


    def rotation(self) -> int:
        ''' 旋转角度
        
        Parameters
        ----------
        
        
        Return 
        ----------
        0, 1, 2, 3
        '''
        return self.__device.rotation()
    
    def package_info(self, package_name: str) -> None | dict:
        ''' 应用信息
        
        Parameters
        ----------
        
        
        Return
        ----------
        {"version_name": "1.1.7", "version_code": "1007"}
        '''
        
        return self.__device.package_info(package_name)
    
    def send_keys(self, text: str) -> None | dict:
        ''' 打印字
        
        Parameters
        ----------
        
        
        Return
        ----------
        
        '''
        
        return self.__device.send_keys(text)
    
    def keyevent(self, text: int|str):
        ''' 输入按键
        
        Parameters
        ----------
        
        
        Return
        ----------
        
        '''
        
        return self.__device.keyevent(text)
    
    def switch_screen(self, on: bool):
        ''' 输入按键
        
        Parameters
        ----------
        on: bool : 亮屏 true、关屏 false
        
        Return
        ----------
        
        '''
        
        return self.__device.switch_screen(on)
    
    def screenshot(self, image_path: str):
        ''' 截图并保存到本地
        
        Parameters
        ----------
        image_path: str 图片本地路径
        
        Return
        ----------
        
        '''
        
        pilimg = self.__device.screenshot()
        pilimg.save(image_path)
        return image_path
    
    def app_current(self) -> None | dict:
        ''' 获取当前应用信息
        
        Parameters
        ----------
        
        Return
        ----------
        dict 
        '''
        info = self.__device.app_current()
        result = {
            "package_name": info.package,
            "activity": info.activity,
            "pid" : info.pid
        }
        return result
    
    def app_start(self, package_name : str, activity : str = None):
        ''' 开启应用
        
        Parameters
        ----------
        package_name : str 开启应用的包名
        
        activity : str = None 入口的activity
        
        Return
        ----------
        '''
        if activity is None:
            content = self.__device.shell(f"dumpsys package {package_name}").split("\n")
            index = 0
            for line in content:
                line : str = line
                line = line.strip()
                if line.__contains__('android.intent.action.MAIN'):
                    break;
                index += 1
            activity = content[index + 1]
            activity = activity.strip()
            activity = activity.split(' ')[1]
            activity = activity.split('/')[1]


        return self.__device.shell(f'am start {package_name}/{activity}')
    
    def app_stop(self, package_name : str):
        ''' 停止应用
        
        Parameters
        ----------
        package_name : str 应用的包名
        
        Return
        ----------
        '''
        
        return self.__device.app_stop(package_name)
    

    def shell(self, text : str, convertOutputToString=True) -> str | bytes:
        ''' 使用adb运行命令行
        
        Parameters
        ----------
        
        
        Returns
        -------
        str | bytes 命令行返回的内容
        
        '''
        return self.__device.shell(text)
    

    def unlock(self, check_status : bool=False) -> bool:
        ''' 解锁手机（需要手机不设置密码）
        
        Parameters
        ----------
        check_status 是否检查状态，为True时，如果已经开锁，则不执行
        
        Returns
        -------
        bool
        
        '''
        # 解锁手机
        if check_status:
            screen_on = self.__device.is_screen_on()
            if screen_on:
                return;
        self.__device.switch_screen(True)
        time.sleep(1)
        self.slide(begin = (176, 1647), end=(747, 940))
        time.sleep(1)
        


if __name__ == '__main__':


    adb = Adb(seril='127.0.0.1:16384')
    adb.connect()
    adb.app_start('com.gonsin.conference.app')
    # adb.find_element("text", "上滑解锁")
    print(adb.shell("echo TEST1"))
