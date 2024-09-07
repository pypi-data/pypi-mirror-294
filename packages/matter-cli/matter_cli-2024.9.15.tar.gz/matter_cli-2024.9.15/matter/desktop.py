# -*- encoding: utf-8 -*-
'''
@File		:	desktop.py
@Time		:	2024/01/05 14:39:48
@Author		:	dan
@Description:	matter测试框架桌面控制入口
'''



import random
import time
from matter.manager.group_manager import GroupManager


def mouse_click(arr: tuple | list, button : str = 'left'):
    """ 模拟点击

    Parameters
    ----------
    arr : array
        两种格式
        1、[x, y]，表示点击确定的点
        2、[x1, y1, x2, y2]，表示点击某个区域（会在该区域点击随机的点）

    button: str
        'left' : 左键（默认）
        'right' : 右键
        'middle' : 中键

    Returns
    -------
    bool
        执行成功 True
        执行失败 False
    """
    
    client = GroupManager().current_client()
    if client.desktop is None:
        return None
    if len(arr) == 2:
        x = arr[0]
        y = arr[1]
    elif len(arr) == 4:
        x = arr[0]
        y = arr[1]
        x1 = arr[2]
        y1 = arr[3]

    touch_x = None
    if x1 and y1:
        touch_x = random.randrange(x, x1)
        touch_y = random.randrange(y, y1)
    else:
        touch_x = x;
        touch_y = y;
    client.desktop.mouse_click(touch_x, touch_y)
    if client.interval > 0:
        time.sleep(client.interval)
    return True


def slide(begin : tuple | list, end : tuple | list, speed : float | int = 200):
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
    pass





def touch_by_image(image_path : str):
    """ 匹配图片并且点击（会将匹配分数最高的进行点击）

    Parameters
    ----------
    image_path : str
        图片在本地的位置

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    pass


def touch_by_text(text : str):
    """ 匹配文本内容并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    text : str
        文本内容

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    pass



def touch_by_content(content : str):
    """ 匹配文本内容并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    content : str
        文本内容

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    pass



def touch_by_id(id : str):
    """ 匹配id并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    id : str
        id 的值

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    pass



def touch_by_xpath(xpath : str):
    """ 匹配xpath并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    xpath : str
        xpath 的值

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    pass



def exist_image(image_path : str):
    """ 查找当前应用截图是否存在该截图

    Parameters
    ----------
    image_path : str
        图片在本地的位置

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    pass



def exist_text(text : str):
    """ 查找当前应用是否存在某个文本

    Parameters
    ----------
    text : str
        文本 内容

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    pass



def existContent(content : str):
    """ 查找当前应用是否存在某个文本

    Parameters
    ----------
    content : str
        文本 内容

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    pass



def exist_id(id : str):
    """ 查找当前应用是否存在某个id

    Parameters
    ----------
    id : str
        id 内容

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    pass



def exist_xpath(xpath : str):
    """ 查找当前应用是否存在某个xpath

    Parameters
    ----------
    xpath : str
        xpath 内容

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    pass



def input(text : str):
    """ 模拟键盘输入文本

    Parameters
    ----------
    text : str
        文本 内容

    Returns 
    -------
    bool
        输入成功 True
        输入失败 False
    """
    pass



def monkey(time : int = None):
    """ 执行安卓monkey测试

    Parameters
    ----------
    time : int
        执行时长，单位毫秒，0或None表示永久执行

    Returns 
    -------
    bool
        执行成功 True
        执行失败 False
    """
    pass
