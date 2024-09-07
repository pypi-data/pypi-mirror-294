# -*- encoding: utf-8 -*-
'''
@File		:	adb_client.py
@Time		:	2024/01/09 09:46:16
@Author		:	dan
@Description:   使用了androidviewclient作为技术实现，详情查看 https://github.com/dtmilano/AndroidViewClient
'''
import random
from com.dtmilano.android.viewclient import ViewClient, KEY_EVENT
from com.dtmilano.android.adb import adbclient
from apkfile import ApkFile, XapkFile, ApkmFile, ApksFile
from culebratester_client import Text, ObjectRef

class Adb:
    ''' 
    adb 连接封装
    '''
    

    @property
    def connected(self) -> bool:
        ''' 
        是否已连接
        '''
        return self.__connected

    @property
    def device(self) -> adbclient.AdbClient:
        return self.__device
    
    
    def __init__(self, seril: str = 'local', package_name : str = None) -> None:
        self.__connected = False
        self.__device = None
        if seril == 'local':
            self.__ip = 'local'
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
        self.__package_name = package_name


    def connect(self) -> bool:
        ''' 连接到安卓设备
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool 连接成功与失败
        
        '''
        if not self.__device:
            if self.__ip == 'local':
                self.__ip = 'local'
                self.__device, self.__serialno = ViewClient.connectToDeviceOrExit(
                    verbose = False, 
                    ignoresecuredevice = False, 
                    ignoreversioncheck = False
                )
                return
            else:
                self.__device, self.__serialno = ViewClient.connectToDeviceOrExit(
                    verbose=False,
                    ignoresecuredevice=False,
                    ignoreversioncheck=False,
                    serialno=self.__ip + ":" + self.__port.__str__()
                    )
                
            self.__view_client = ViewClient(
                self.__device, self.__serialno,
                forceviewserveruse=False,
                startviewserver=True,
                autodump=False,
                ignoreuiautomatorkilled=True,
                compresseddump=True,
                useuiautomatorhelper=True,
                debug={})
            self.__helper = self.__view_client.uiAutomatorHelper;
            return True
        return False
    


    def shell(self, text : str, convertOutputToString=True) -> str | bytes:
        ''' 使用adb运行命令行
        
        Parameters
        ----------
        
        
        Returns
        -------
        str | bytes 命令行返回的内容
        
        '''
        return self.__device.shell(text, convertOutputToString)
    

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

        self.__view_client.touch(x, y)
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
    

    def is_installed(self, package_name):
        ''' 
        是否安装了某包名
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        packages = self.__device.shell('pm list packages').splitlines()
        return packages.__contains__(package_name)
    

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

        info = self.get_apk_info(apk_path)
        installed = self.is_installed(info.package_name)
        if uninstall and installed:
            self.__view_client.uninstallPackage(info.package_name)
            self.__view_client.installPackage(apk=apk_path)
        elif not installed:
            self.__view_client.installPackage(apk=apk_path)
        return True
    
    


    def slide(self, begin : tuple | list, end : tuple | list, speed : float | int = 200):
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

        self.__view_client.swipe(begin[0], begin[1], end[0], end[1], steps=speed * 2.0)
        return True
    

    def find_element(self, by: str, value : str) -> ObjectRef:
        """ 查找元素

        Parameters
        ----------
        by: str 通过什么查找
        
        value : str 相应的值

        Returns
        -------
        """
        if not self.__connected:
            self.connect()

        body = {}
        body['pkg'] = self.__package_name
        if by == 'id':
            body['res'] = self.__package_name + ":id/" + value
            return self.__helper.until.find_object(body=body)
        elif by == 'text':
            body['text'] = value
            return self.__helper.until.find_object(body=body)
        
    def touch_element(self, element : dict) -> bool:
        ''' 根据元素点击
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__connected:
            self.connect()
        x1, y1, x2, y2 = element['bounds']
        touch_x = random.randrange(x1, x2)
        touch_y = random.randrange(y1, y2)
        self.touch(touch_x, touch_y)

    def window_size(self) -> tuple:
        ''' 窗口大小
        
        Parameters
        ----------
        
        
        Return
        ----------
        tuple 例如 (1000, 1920)
        '''
        
        display = self.__device.getLogicalDisplayInfo()
        return (display.width, display.height);


    def rotation(self) -> int:
        ''' 旋转角度
        
        Parameters
        ----------
        
        
        Return 
        ----------
        0, 1, 2, 3
        '''
        display = self.__device.getLogicalDisplayInfo()
        return display.rotation
    
    def package_info(self, package_name: str) -> None | dict:
        ''' 应用信息
        
        Parameters
        ----------
        
        
        Return
        ----------
        {"version_name": "1.1.7", "version_code": "1007"}
        '''
        
        version_name = self.__device.shell(f"dumpsys package {package_name} | grep versionName")
        version_name = version_name.split("=")[1]
        version_code = self.__device.shell(f"dumpsys package {package_name} | grep versionCode")
        version_code = version_code.split("=")[1]

        return {"version_name": version_name, "version_code" : version_code}
    
    def send_keys(self, text: str) -> None | dict:
        ''' 打印字
        
        Parameters
        ----------
        
        
        Return
        ----------
        
        '''
        
        return self.__device.type(text)
    
    def keyevent(self, text: int|str):
        ''' 输入按键
        
        Parameters
        ----------
        
        
        Return
        ----------
        
        '''
        
        return self.__view_client.pressKeyCode(text)
    
    def switch_screen(self, on: bool):
        ''' 输入按键
        
        Parameters
        ----------
        on: bool : 亮屏 true、关屏 false
        
        Return
        ----------
        
        '''
        # 亮屏
        if on and not self.__device.isScreenOn():
            self.__device.unlock()
            return
        
        # 关屏
        if not on and self.__device.isScreenOn():
            self.__device.press('26')

        return True
    
    def screenshot(self, image_path: str):
        ''' 截图并保存到本地
        
        Parameters
        ----------
        image_path: str 图片本地路径
        
        Return
        ----------
        
        '''
        
        pilimg = self.__device.takeSnapshot(reconnect=True)
        pilimg.save(image_path)
    
    def app_current(self) -> None | dict:
        ''' 获取当前应用信息
        
        Parameters
        ----------
        
        Return
        ----------
        dict 
        '''
        
        return self.__device.getFocusedWindow()
    
    
    
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
    

    
    def app_start(self, package_name : str, activity : str = None):
        ''' 开启应用
        
        Parameters
        ----------
        package_name : str 开启应用的包名
        
        activity : str = None 入口的activity
        
        Return
        ----------
        '''
        if activity:
            package_name += "/" + activity
        return self.__device.startActivity(package_name)
    
    def app_stop(self, package_name : str):
        ''' 停止应用
        
        Parameters
        ----------
        package_name : str 应用的包名
        
        Return
        ----------
        '''
        
        return self.__device.forceStop(package_name)


if __name__ == '__main__':


    adb = Adb()
    adb.connect()
    adb.switch_screen(True)
    print(adb.shell("echo TEST1"))
