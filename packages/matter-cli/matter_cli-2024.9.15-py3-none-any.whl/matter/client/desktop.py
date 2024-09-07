# -*- encoding: utf-8 -*-
'''
@File		:	desktop.py
@Time		:	2024/01/05 10:27:59
@Author		:	dan
@Description:	桌面操作，技术使用的是pyautogui，参考 https://www.zhihu.com/tardis/zm/art/302592540?source_id=1005
'''
import pyautogui
import pyperclip
import subprocess

class Desktop:
    '''
    桌面程序测试接口封装类，可以支持linux、windows、macos等桌面系统
    '''
    def __init__(self, bin : str, window_size : str = "max") -> None:
        ''' 
        
        Parameters
        ----------
        bin : str 可执行文件的路径
        
        Return
        ----------
        '''
        
        self.__bin = bin
        self.__process : subprocess.Popen = None

        pass


    def open(self) -> None:
        ''' 开始运行 可执行文件
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if self.__process:
            return;
        self.__process = subprocess.Popen(self.__bin)
        pass


    def close(self) -> None:
        ''' 开始运行 可执行文件
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__process:
            return;
        self.__process.kill()
        pass


    def get_size(self) -> pyautogui.Size:
        ''' 获取屏幕尺寸
        
        Parameters
        ----------
        
        
        Returns
        -------
        Size
        
        '''
        return pyautogui.size()


    def mouse_position(self) -> pyautogui.Point:
        ''' 获取鼠标位置
        
        Parameters
        ----------
        
        
        Returns
        -------
        Size
        
        '''
        return pyautogui.position()

    def mouse_move(self, x : int, y : int, duration=0.0) -> None:
        ''' 移动鼠标
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        pyautogui.moveTo(x, y, duration)
        pass    


    def mouse_down(self, x : int = None, y : int = None, button : str = 'left') -> None:
        ''' 按下鼠标
        
        Parameters
        ----------

        x : int = None 鼠标点击位置（可选）
        
        y : int = None 鼠标点击位置（可选）

        button : str 鼠标的按键 'left', 'middle', 'right', 1, 2, or 3
        
        Returns
        -------
        None
        
        '''
        pyautogui.mouseDown(x, y, button=button)
        pass    


    def mouse_up(self, x : int = None, y : int = None, button : str = 'left') -> None:
        ''' 释放鼠标
        
        Parameters
        ----------

        x : int = None 鼠标点击位置（可选）
        
        y : int = None 鼠标点击位置（可选）

        button : str 鼠标的按键 'left', 'middle', 'right', 1, 2, or 3
        
        Returns
        -------
        None
        
        '''
        pyautogui.mouseUp(x, y, button=button)
        pass    


    def mouse_click(self, x : int = None, y : int = None, button : str = 'left') -> None:
        ''' 点击鼠标
        
        Parameters
        ----------

        x : int = None 鼠标点击位置（可选）
        
        y : int = None 鼠标点击位置（可选）

        button : str 鼠标的按键 'left', 'middle', 'right', 1, 2, or 3
        
        Returns
        -------
        None
        
        '''
        pyautogui.click(x=x, y=y, button=button)
        pass    


    def mouse_double_click(self, x : int = None, y : int = None, button : str = 'left') -> None:
        ''' 点击鼠标
        
        Parameters
        ----------

        x : int = None 鼠标点击位置（可选）
        
        y : int = None 鼠标点击位置（可选）

        button : str 鼠标的按键 'left', 'middle', 'right', 1, 2, or 3
        
        Returns
        -------
        None
        
        '''
        pyautogui.click(x=x, y=y, button=button, clicks=2)
        pass    


    def mouse_scroll(self, clicks : float = 1, x : int = None, y : int = None, button : str = 'left') -> None:
        ''' 点击鼠标
        
        Parameters
        ----------
        clicks : float = 1 正数，向上滚动，负数，向下滚动

        x : int = None 鼠标位置（可选）
        
        y : int = None 鼠标位置（可选）

        button : str 鼠标的按键 'left', 'middle', 'right', 1, 2, or 3
        
        Returns
        -------
        None
        
        '''
        pyautogui.scroll(clicks, x=x, y=y, button=button, clicks=2)
        pass    


    def press(self, keys : str | list, presses : int = 1, interval : float =0.0) -> None:
        ''' 键盘操作 模拟打字
        该方法只是模拟键盘打字，不能直接输入中文，输入中文请使用 input_text 方法
        Parameters
        ----------
        keys : str | list 输入的字符串
        
        presses : int = 1 重复次数
        
        interval : float =0.0 每次输入的间隔

        Returns
        -------
        None
        
        '''
        pyautogui.press(keys, presses, interval)


    def hotkey(self, keys : list | tuple) -> None:
        ''' 输入组合键

        该方法和 press的区别，是press是逐个输入，hotkey是一次性输入

        Parameters
        ----------

        Returns
        -------
        None
        
        '''
        pyautogui.hotkey(keys[:])


    def input_text(self, text : str) -> None:
        ''' 输入文字

        Parameters
        ----------
        text : str 文字内容

        Returns
        -------
        None
        
        '''
        origin = pyperclip.paste()
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        pyperclip.copy(origin)


    def screenshot(self, image_path: str, region : tuple[int, int, int, int] = None) -> None:
        ''' 截图
        
        Parameters
        ----------
        image_path: str 本地保存图片的路径
        
        region : tuple[int, int, int, int] = None 截图大小，默认为全屏

        Returns
        -------
        None
        
        '''
        pyautogui.screenshot(image_path, region)
        pass    


    def locate_on_screen(self, image_path: str, region : tuple[int, int, int, int] = None) -> tuple:
        ''' 根据图片在屏幕中定位
        
        Parameters
        ----------
        image_path: str 比较的本地图片
        
        region : tuple[int, int, int, int] = None 搜索区域，默认全屏

        Returns
        -------
        None
        
        '''
        return pyautogui.locateOnScreen(image = image_path, region=region)