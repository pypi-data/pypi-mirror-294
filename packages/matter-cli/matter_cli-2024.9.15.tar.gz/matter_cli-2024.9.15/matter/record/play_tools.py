# -*- encoding: utf-8 -*-
'''
@File		:	play_tools.py
@Time		:	2024/01/17 14:37:14
@Author		:	dan
@Description:	回放录制的脚本
'''

import json
import pynput
import time
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import threading
import sys

class PlayTools:
    ''' 回放录制的脚本
    
    '''

    BUTTONS = {}

    if sys.platform == 'win32':
        BUTTONS["left"] = Button.left
        BUTTONS["right"] = Button.right 
        BUTTONS["middle"] = Button.middle 
        BUTTONS["x1"] = Button.x1 
        BUTTONS["x2"] = Button.x2
    
    if sys.platform == "linux":
        BUTTONS["button8"] = Button.button8
        BUTTONS["button9"] = Button.button9 
        BUTTONS["button10"] = Button.button10 
        BUTTONS["button11"] = Button.button11 
        BUTTONS["button12"] = Button.button12 
        BUTTONS['button13'] = Button.button13 
        BUTTONS["button14"] = Button.button14 
        BUTTONS["button15"] = Button.button15 
        BUTTONS["button16"] = Button.button16 
        BUTTONS["button17"] = Button.button17 
        BUTTONS["button18"] = Button.button18 
        BUTTONS["button19"] = Button.button19 
        BUTTONS["button20"] = Button.button20 
        BUTTONS["button21"] = Button.button21 
        BUTTONS["button22"] = Button.button22 
        BUTTONS["button23"] = Button.button23 
        BUTTONS["button24"] = Button.button24 
        BUTTONS["button25"] = Button.button25 
        BUTTONS["button26"] = Button.button26 
        BUTTONS["button27"] = Button.button27 
        BUTTONS["button28"] = Button.button28 
        BUTTONS["button29"] = Button.button29 
        BUTTONS["button30"] = Button.button30 
        BUTTONS["scroll_down"] = Button.scroll_down 
        BUTTONS["scroll_left"] = Button.scroll_left 
        BUTTONS["scroll_right"] = Button.scroll_right 
        BUTTONS["scroll_up"] = Button.scroll_up 
        

    @property
    def started(self) -> bool:
        return self.__started

    def __init__(self, record_file) -> None:
        self.__record_file = record_file
        with open(record_file) as f:
            # 将记录的命令写入命令列表
            self.__command_list = json.loads(f.read())
        self.__mouse = pynput.mouse.Controller()
        self.__keyboard = pynput.keyboard.Controller()
        self.__play_thread = threading.Thread(target=self.play)
        self.__started = False;


    def start(self) -> None:
        ''' 开始执行脚本
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        if (self.__started):
            return
        self.__started = True
        self.__play_thread.start()



    def play(self) -> None:
        ''' 播放脚本
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        for command in self.__command_list:
            # 如果是点击记录
            action = command['action']
            data = command['data']
            delay = command['time']
            time.sleep(delay)

            # 如果是单击
            if action == "mouse_click":
                # 将鼠标移动到记录中的位置
                self.__mouse.position = (data[0], data[1])
                self.__mouse.click(PlayTools.BUTTONS[command['data'][2]])
            # 如果是双击
            elif action == "mouse_move":
                # 将鼠标移动到记录中的位置
                self.__mouse.position = (data[0], data[1])
            elif action == "mouse_scroll":
                # 滚动鼠标
                self.__mouse.scroll(data[2], data[3])

            # 如果是按键按下
            elif action == "key_down":
                # 如果是特殊按键,会记录成Key.xxx,这里判断是不是特殊按键
                if data[0][:3] == "Key":
                    # 按下按键
                    self.__keyboard.press(eval(data[0], {}, {
                        "Key": pynput.keyboard.Key
                    }))
                else:
                    # 如果是普通按键,直接按下
                    if "<255>" == data[0]:
                        continue
                    # print(data[0])    
                    # print(data[0].split("'")[1])
                    # keyboard.press(data[0].split("'")[1])
                    self.__keyboard.press(data[0])
            # 如果是按键释放
            elif action == "key_up":
                # 如果是特殊按键
                if data[0][:3] == "Key":
                    # 按下按键
                    self.__keyboard.release(eval(data[0], {}, {
                        "Key": pynput.keyboard.Key
                    }))
                else:
                    # 普通按键直接按下
                    if "<255>" == data[0]:
                        continue
                    # print(data[0])    
                    # print(data[0].split("'")[1])
                    # keyboard.release(data[0].split("'")[1])
                    self.__keyboard.release(data[0])
            # command[2]代表此操作距离开始操作所经过的时间,用它减去已经经过的时间就是距离下一次操作的时间
            # time.sleep(command[2] - sTime)
            # 更新时间
            # sTime = command[2]


if __name__ == '__main__':
    play = PlayTools(record_file='record.json')
    play.play()