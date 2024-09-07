# -*- encoding: utf-8 -*-
'''
@File		:	record_window.py
@Time		:	2024/01/18 09:57:46
@Author		:	dan
@Description:	录制屏幕的小窗口
'''


import os 
import time   
import json    
import threading    
import tkinter  
from tkinter import Tk, messagebox
from play_tools import PlayTools
from record_tools import RecordTools
import pynput    
import ctypes



class RecordWindow:
    '''
    录制屏幕操作的窗口工具
    '''
    def __init__(self) -> None:
        self.__top = tkinter.Tk()
        self.__top.title('matter操作录制工具')
        self.__top.geometry('500x250')
 
        frame1 = tkinter.Frame(self.__top)
        frame1.pack(side='top')
        l1 = tkinter.Label(frame1,
                           text='【1----录制操作】\n注意：\n按 Ctrl + W 开始录制\n按 Ctrl + Q 退出录制')
        l1.pack()
        self.__record_button = tkinter.Button(frame1,
                            text='录制',
                            width=15, height=2,
                            command=self.switch_record)
        self.__record_button.pack()
        
        self.__top.bind('<Control-w>', self.start_record)
        # self.__top.bind('<Control-q>', self.stop_record)


        frame2 = tkinter.Frame(self.__top)
        frame2.pack(side='bottom')
        l2 = tkinter.Label(frame2,
                           text='【2----执行操作】')
        l2.pack()
        self.__play_button = tkinter.Button(frame2,
                            text='执行',
                            width=15, height=2,
                            command=self.start_play)
        self.__play_button.pack()
        l3 = tkinter.Label(frame2,
                           text='请输入执行次数，默认为1次')
        l3.pack()
        self.__count = tkinter.StringVar()
        e1= tkinter.Entry(frame2, textvariable=self.__count)
        e1.pack()
 
        self.__record_file = 'record.json'
        self.__recorder = RecordTools()

        self.__top.mainloop()
        


    def switch_record(self, event) -> None:
        ''' 关闭、开启录制
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if self.__recorder.started:
            self.__recorder.stop()
            self.__record_button.config(state='normal')
            self.__play_button.config(state='normal')
            return
        self.__recorder.start()
        self.__record_button.config(state='disabled')
        self.__play_button.config(state='disabled')



    def start_record(self, event) -> None:
        ''' 开始录制
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if self.__recorder.started:
            return
        self.__recorder.start()
        self.__record_button.config(state='disabled')
        self.__play_button.config(state='disabled')
        
    
    def stop_record(self, event) -> None:
        ''' 结束录制
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if self.__recorder.started:
            self.__recorder.stop()
            self.__recorder.save(self.__record_file)
            self.__record_button.config(state='normal')
            self.__play_button.config(state='normal')


    def start_play(self, event) -> None:
        ''' 开始回放
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__recorder:
            self.__recorder = RecordTools(self.__record_file)
        self.__recorder.start()
        


if __name__ == '__main__':
    window = RecordWindow()