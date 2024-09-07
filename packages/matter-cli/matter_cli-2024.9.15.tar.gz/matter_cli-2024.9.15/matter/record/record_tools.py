# -*- encoding: utf-8 -*-
'''
@File		:	record_tools.py
@Time		:	2024/01/17 10:19:20
@Author		:	dan
@Description:	录制鼠标键盘的工具类
'''

import pynput
import time
import json
import threading
import sys
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

class RecordTools:

    @property
    def started(self) -> bool:
        return self.__started

    '''
    录制鼠标键盘的封装类
    '''
    def __init__(self, started_callback = None, stop_callback = None) -> None:

        self.__command_list : list[dict] = []
        '''
        命令顺序
        '''
        # {
        #     action: 'down/up',

        #     具体按下的键,传进来的参数并不是一个字符串,而是一个对象,如果按下的是普通的键,会记录下键对应的字符,否则会使一个"Key.xx"的字符串
        #     position: (x, y),
        #     action_time : 484
        # }


        self.__start_time = time.time()
        self.__mouse_x_old = 0
        self.__mouse_y_old = 0
        self.__mouse_t_old = 0
        self.__started = False
        self.__keyboard_listener = pynput.keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.__mouse_lisetner = pynput.mouse.Listener(on_click=self.on_mouse_click, on_move=self.on_mouse_move, on_scroll=self.on_mouse_scroll)
        self.__last_time = time.time()
        self.__started_callback = started_callback
        self.__stop_callback = stop_callback
        pass


    def record_keyboard(self) -> None:
        ''' 录制键盘
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        with self.__keyboard_listener as listener:
            listener.join()


    def record_mouse(self) -> None:
        ''' 录制鼠标
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        with self.__mouse_lisetner as listener:
            listener.join()
        

    def stop(self) -> None:
        ''' 停止录制
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__mouse_lisetner.stop()
        self.__keyboard_listener.stop()
        self.__started = False
        if self.__stop_callback:
            self.__stop_callback(self)



    def start(self) -> None:
        ''' 开始录制
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        # 进行监听
        if self.__started:
            return;
        self.__started = True
        self.__last_time = time.time()
        self.__keyboard_thread = threading.Thread(target=self.record_keyboard)
        self.__mouse_thread = threading.Thread(target=self.record_mouse)
        self.__keyboard_thread.start()
        self.__mouse_thread.start()
        if self.__started_callback:
            self.__started_callback(self)
        print("开始录制键盘鼠标操作，按 ctrl + q 退出录制")

    def on_key_press(self, key) -> None:
        ''' 当按键按下时记录
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        k = keyboard.Key.ctrl_l
        key = str(key).strip("'")
        # if key.startswith('Key.'):
        #     key = key[4:]

        # ctrl + q 退出录制
        if key == '\\x11':    
            #如果是esc 则退出录制
            self.__running = False  
            # mouse=pynput.mouse.Controller()    
            # mouse.click(pynput.mouse.Button.left)   
            self.stop()
            return False   
        

        self.__command_list.append({
            "action" : "key_down",    #操作模式
            "data": (str(key).strip("'"),),    
            #操作距离程序开始运行的秒数
            "time": time.time() - self.__last_time    
        })
        self.__last_time = time.time()
    
    def on_key_release(self, key):    #但按键松开时记录
        ''' 当按键释放时记录
        
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        
        self.__command_list.append({
            "action" : "key_up",    #操作模式
            "data": (str(key).strip("'"),),    
            "time": time.time() - self.__last_time    
        })
        self.__last_time = time.time()


    def on_mouse_scroll(self, x, y, scroll_left, scroll_up) -> None:
        ''' 鼠标滚动事件
        
        Parameters
        ----------
        x, y,  鼠标当前位置
        
        scroll_left  左右滚动方向，1为往左，0为往右
        
        scroll_up   上下滚动方向，1为往上，-1为往下
        
        Returns
        -------
        None
        
        '''
        # if scroll_left:
        #     scroll_left = 1
        # else:
        #     if scroll_up == 1 or scroll_up == -1:
        #         scroll_left = 0
        #     else:
        #         scroll_left = -1
        # print(f"on_mouse_scroll ({x}, {y}, {scroll_left}, {scroll_up})")
                

        if not self.__started:    #如果已经不在运行了
            return False    #退出监听
        self.__command_list.append({
            "action": "mouse_scroll",  # 操作模式
            "data": (x, y, scroll_left, scroll_up),  # 分别是鼠标的坐标和按下的按键
            "time": time.time() - self.__last_time  # 操作距离程序开始运行的秒数
        })
        self.__last_time = time.time()
        return True


    def on_mouse_move(self, x, y) -> None:
        ''' 鼠标拖动事件
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        # print(f"on_mouse_move ({x}, {y})")
        
        if not self.__started:    #如果已经不在运行了
            return False    #退出监听
        self.__command_list.append({
            "action":"mouse_move",  # 操作模式
            "data": (x, y),  # 分别是鼠标的坐标和按下的按键
            "time": time.time() - self.__last_time  # 操作距离程序开始运行的秒数
        })
        self.__last_time = time.time()
        return True
    

    def join(self) -> None:
        ''' 暂停录制线程
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        self.__mouse_thread.join()


    def on_mouse_click(self, x, y, button : Button, down):
        ''' 
        鼠标按下事件
        Parameters
        ----------
        
        
        Return
        ----------
        '''
        if button == Button.left:
            button = 'left'
        if button == Button.middle:
            button = 'middle'
        if button == Button.right:
            button = 'right'
        if button == Button.x1:
            button = 'x1'
        if button == Button.x2:
            button = 'x2'
        if sys.platform == "linux":
            if button == Button.button8 : button = 'button8'
            if button == Button.button9 : button = 'button9'
            if button == Button.button10 : button = 'button10'
            if button == Button.button11 : button = 'button11'
            if button == Button.button12 : button = 'button12'
            if button == Button.button13 : button = 'button13'
            if button == Button.button14 : button = 'button14'
            if button == Button.button15 : button = 'button15'
            if button == Button.button16 : button = 'button16'
            if button == Button.button17 : button = 'button17'
            if button == Button.button18 : button = 'button18'
            if button == Button.button19 : button = 'button19'
            if button == Button.button20 : button = 'button20'
            if button == Button.button21 : button = 'button21'
            if button == Button.button22 : button = 'button22'
            if button == Button.button23 : button = 'button23'
            if button == Button.button24 : button = 'button24'
            if button == Button.button25 : button = 'button25'
            if button == Button.button26 : button = 'button26'
            if button == Button.button27 : button = 'button27'
            if button == Button.button28 : button = 'button28'
            if button == Button.button29 : button = 'button29'
            if button == Button.button30 : button = 'button30'
            if button == Button.scroll_down : button = 'scroll_down'
            if button == Button.scroll_left : button = 'scroll_left'
            if button == Button.scroll_right : button = 'scroll_right'
            if button == Button.scroll_up : button = 'scroll_up'
        # print(f"on_mouse_click ({x}, {y}, {str(button)}, {str(down)})")
            

        if not self.__started:    #如果已经不在运行了
            return False    #退出监听
        self.__command_list.append({
            "action": "mouse_click",  # 操作模式
            "data": (x, y, str(button), str(down)),  # 分别是鼠标的坐标和按下的按键
            "time": time.time() - self.__last_time  # 操作距离程序开始运行的秒数
        })
        self.__last_time = time.time()
        return True
        
        # if self.__mouse_x_old == x and self.__mouse_y_old == y:
        #     if time.time() - self.__mouse_t_old > 0.3: #如果两次点击时间小于0.3秒就会判断为双击 否则就是单击
        #         self.__command_list.append((
        #             "click",  # 操作模式
        #             (x, y, str(button), str(down)),  # 分别是鼠标的坐标和按下的按键
        #             time.time() - self.__start_time  # 操作距离程序开始运行的秒数
        #         ))


        #     else:
        #         self.__command_list.pop(0)  #删除前一个
        #         self.__command_list.append((
        #             "double-click",  # 操作模式
        #             (x, y, str(button)),  # 分别是鼠标的坐标和按下的按键
        #             time.time() - self.__start_time  # 操作距离程序开始运行的秒数
        #         ))

        # else:
        #     self.__command_list.append((
        #         "click",  # 操作模式
        #         (x, y, str(button)),  # 分别是鼠标的坐标和按下的按键
        #         time.time() - self.__start_time  # 操作距离程序开始运行的秒数
        #     ))
        # self.__mouse_x_old = x
        # self.__mouse_y_old = y
        # self.__mouse_t_old = time.time()
 
    def save(self, path : str):    #保存为文件,参数分别为操作记录和保存位置
        ''' 
        
        Parameters
        ----------
        path : 保存文件的位置
        
        Return
        ----------
        '''
        
        with open(path,"w") as f:
            f.write(json.dumps(self.__command_list))    #使用json格式写入


if __name__ == '__main__':
    record = RecordTools()
    record.start()
    record.join()
    record.save('record.json')
    record.stop()