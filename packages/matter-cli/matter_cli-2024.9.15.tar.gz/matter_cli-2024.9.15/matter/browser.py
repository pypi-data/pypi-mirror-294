# -*- encoding: utf-8 -*-
'''
@File		:	browser.py
@Time		:	2024/01/05 14:40:09
@Author		:	dan
@Description:	matter测试框架，浏览器入口
'''

from matter.group import Group
from matter.manager.group_manager import GroupManager
import matter.utils.system_utils as system_utils
import os
import threading
import cv2
import random
import time
from selenium.webdriver.common.keys import Keys

def touch(arr: tuple | list, button : str = 'left'):
    """ 模拟点击

    Parameters
    ----------
    arr : array
        两种格式
        1、[x, y]，表示点击确定的点
        2、[x1, y1, x2, y2]，表示点击某个区域（会在该区域点击随机的点）

    button : str 
        按钮类型，left、right

    Returns
    -------
    bool
        执行成功 True
        执行失败 False
    """
    client = GroupManager().current_client()
    if client.browser is None:
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
    if button == 'left':
        client.browser.click(touch_x, touch_y)
    if button == 'right':
        client.browser.context_click(touch_x, touch_y)
    if client.interval > 0:
        time.sleep(client.interval)
    return True


def slide(begin : tuple | list, end : tuple | list, speed : float | int = 200):
    """ 鼠标点击拖动

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
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    client.browser.slide(begin, end, speed)
    if client.interval > 0:
        time.sleep(client.interval)
    return True





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
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    screen_image = image_path + ".screen.jpg"
    client.browser.screenshot(screen_image);
    img1 = cv2.imread(screen_image)
    img2 = cv2.imread(image_path)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    # 找到最大匹配值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 返回最大匹配位置的坐标
    if max_val > 0.8:
        x, y = max_loc
        client.browser.click(x, y)
        os.remove(screen_image)
    else:
        os.remove(screen_image)
        system_utils.exit(f"找不到匹配的图片{image_path}")
    if client.interval > 0:
        time.sleep(client.interval)
    return True


def touch_by_class(clazz : str):
    """ 匹配class内容并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    clazz : str
        class内容

    Returns 
    -------
    bool
        点击成功返回 True
        查找不到返回 False
    """
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('class name', clazz)
    if type(element) == list:
        if len(element) == 0:
            system_utils.exit('找不到class={clazz}的元素')
        element = element[0]
    client.browser.click_by('class name', clazz)
    if client.interval > 0:
        time.sleep(client.interval)
    return True


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
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('id', id)
    if type(element) == list:
        if len(element) == 0:
            system_utils.exit('找不到class={clazz}的元素')
        element = element[0]
    client.browser.click_by('id', id)
    if client.interval > 0:
        time.sleep(client.interval)
    return True



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
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('xpath', xpath)
    if type(element) == list:
        if len(element) == 0:
            system_utils.exit('找不到class={clazz}的元素')
        element = element[0]
    client.browser.click_by('xpath', xpath)
    if client.interval > 0:
        time.sleep(client.interval)
    return True



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
    client = GroupManager().current_client()
    if client.browser is None:
        return None

    screen_image = image_path + ".screen.jpg"
    client.browser.screenshot(screen_image);
    img1 = cv2.imread(screen_image)
    img2 = cv2.imread(image_path)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    # 找到最大匹配值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 返回最大匹配位置的坐标
    if max_val > 0.8:
        os.remove(screen_image)
        return True
    else:
        os.remove(screen_image)
        system_utils.exit(f"找不到匹配的图片{image_path}")
    return False



def exist_class(clazz : str):
    """ 查找当前应用是否存在某个class

    Parameters
    ----------
    clazz : str
        class 内容

    Returns 
    -------
    bool
        查找到返回 True
        查找不到返回 False
    """
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('class name', clazz)
    if type(element) == list:
        if len(element) == 0:
            return False
        element = element[0]

    if not element:
        return False
    return True;



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
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('id', id)
    if type(element) == list:
        if len(element) == 0:
            return False
        element = element[0]

    if not element:
        return False
    return True;



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
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    element = client.browser.find_element('xpath', xpath)
    if type(element) == list:
        if len(element) == 0:
            return False
        element = element[0]

    if not element:
        return False
    return True;



def input(text : str):
    """ 输入文本

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
    
    client = GroupManager().current_client()
    if client.browser is None:
        return None
    client.browser.send_keys(text)
    if client.interval > 0:
        time.sleep(client.interval)
    return True




def keyevent(key : str | int | tuple):
    """ 模拟键盘操作

    Parameters
    ----------
    key : str
        str : 表示输入字符串
        int : 表示输入键盘功能键
        tuple : 表示输入组合键

    Returns 
    -------
    bool
        输入成功 True
        输入失败 False
    """

    client = GroupManager().current_client()
    if client.browser is None:
        return None
    client.browser.keyevent(key)
    if client.interval > 0:
        time.sleep(client.interval)
    return True