# -*- encoding: utf-8 -*-
'''
@File		:	__init__.py
@Time		:	2024/01/11 14:14:25
@Author		:	dan
@Description:	matter程序入口
'''

if __name__ == '__main__':
    import sys
    sys.path.append(".")

import functools
from matter.manager.case_manager import CaseManager, TestCase
from matter.manager.group_manager import GroupManager
from matter.manager.signal_manager import SignalManager
import matter.utils.system_utils as system_utils
import faker
import os
import time
import random

mock : faker.Faker = faker.Faker()


class Keys:
    """Set of special keys codes."""

    NULL = "\ue000"
    CANCEL = "\ue001"  # ^break
    HELP = "\ue002"
    BACKSPACE = "\ue003"
    BACK_SPACE = BACKSPACE
    TAB = "\ue004"
    CLEAR = "\ue005"
    RETURN = "\ue006"
    ENTER = "\ue007"
    SHIFT = "\ue008"
    LEFT_SHIFT = SHIFT
    CONTROL = "\ue009"
    LEFT_CONTROL = CONTROL
    ALT = "\ue00a"
    LEFT_ALT = ALT
    PAUSE = "\ue00b"
    ESCAPE = "\ue00c"
    SPACE = "\ue00d"
    PAGE_UP = "\ue00e"
    PAGE_DOWN = "\ue00f"
    END = "\ue010"
    HOME = "\ue011"
    LEFT = "\ue012"
    ARROW_LEFT = LEFT
    UP = "\ue013"
    ARROW_UP = UP
    RIGHT = "\ue014"
    ARROW_RIGHT = RIGHT
    DOWN = "\ue015"
    ARROW_DOWN = DOWN
    INSERT = "\ue016"
    DELETE = "\ue017"
    SEMICOLON = "\ue018"
    EQUALS = "\ue019"

    NUMPAD0 = "\ue01a"  # number pad keys
    NUMPAD1 = "\ue01b"
    NUMPAD2 = "\ue01c"
    NUMPAD3 = "\ue01d"
    NUMPAD4 = "\ue01e"
    NUMPAD5 = "\ue01f"
    NUMPAD6 = "\ue020"
    NUMPAD7 = "\ue021"
    NUMPAD8 = "\ue022"
    NUMPAD9 = "\ue023"
    MULTIPLY = "\ue024"
    ADD = "\ue025"
    SEPARATOR = "\ue026"
    SUBTRACT = "\ue027"
    DECIMAL = "\ue028"
    DIVIDE = "\ue029"

    F1 = "\ue031"  # function  keys
    F2 = "\ue032"
    F3 = "\ue033"
    F4 = "\ue034"
    F5 = "\ue035"
    F6 = "\ue036"
    F7 = "\ue037"
    F8 = "\ue038"
    F9 = "\ue039"
    F10 = "\ue03a"
    F11 = "\ue03b"
    F12 = "\ue03c"

    META = "\ue03d"
    COMMAND = "\ue03d"
    ZENKAKU_HANKAKU = "\ue040"


def init(yml_path: str = "./matter.yml"):
    """ 初始化 matter

    Parameters
    ----------
    yml_path : str
        yml 目录，默认为当前目录

    Returns
    -------
    void
        不返回
    """
    group_manager = GroupManager()
    if not group_manager.is_inited:
        group_manager.init(yml_path);
    pass


def sleep(duration : float):
    """ 暂停时间

    Parameters
    ----------
    duration : int 
        暂停的时长 (s)

    Returns
    -------
    void
        不返回
    """
    time.sleep(duration)


def env(name) -> str:
    ''' 
    获取环境变量
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    group = GroupManager().current_group()
    value = group.env(name);
    if value is None:
        value = os.getenv(name);
    return value;


def random_int(a, b) -> int:
    ''' 获取随机的数字
    
    Parameters
    ----------
    
    
    Returns
    -------
    int
    
    '''
    return random.randint(a, b);


def assert_true(value : any, message : str = None, error_code : int = None):
    """ 判断为真，如果不为真，则提示内容

    Parameters
    ----------
    value : any
        需要判断的变量

    message : str
        提示的内容

    error_code : int
        程序结束时返回的错误码

    Returns
    -------
    void
        不返回
    """
    if not value:
        system_utils.exit(message=message, error_code=error_code)


def exit(message : str = None, error_code : int = None):
    """ 正常退出，或错误退出

    Parameters
    ----------
    message : str
        退出时提示的内容

    error_code : int
        程序结束时返回的错误码

    Returns
    -------
    void
        不返回
    """
    system_utils.exit(message=message, error_code=error_code)


def post(signal : str, obj : any = None):
    """ 抛出消息，通常用于异步处理

    Parameters
    ----------
    signal : str
        信号的值

    obj : any = None
        信号携带的信息

    Returns
    -------
    void
        不返回
    """
    signal_manager = SignalManager()
    signal_manager.post_signal(signal=signal, value=obj)



def on(signal : str, callback):
    """ 接收消息，并执行callback的内容

    Parameters
    ----------
    signal : str
        信号的值

    callback
        回调执行的内容，方法的第一个参数为信号值，第二个参数为信号携带的变量

    Returns
    -------
    void
        不返回
    """
    group_manager = GroupManager()
    group = group_manager.current_group()
    signal_manager = SignalManager()
    signal_manager.register_signal(group=group, signal=signal, callback=callback)





def off(signal : str, callback):
    """ 接收消息，并执行callback的内容

    Parameters
    ----------
    signal : str
        信号的值

    callback
        回调执行的内容，方法的第一个参数为信号值，第二个参数为信号携带的变量

    Returns
    -------
    void
        不返回
    """
    group_manager = GroupManager()
    group = group_manager.current_group()
    signal_manager = SignalManager()
    signal_manager.unregister_signal(group=group, signal=signal, callback=callback)



def start(yml : str = 'matter.yml'):
    """ 开始执行测试

    Parameters
    ----------
    yml : str 本地matter.yml的位置，默认为当前目录的matter.yml
    

    Returns
    -------
    void
        不返回
    """
    group_manager = GroupManager()
    if not group_manager.is_inited:
        group_manager.init(yml_path=yml)

    group_manager.start()



def test_case(name : str = None, dependencies : str | list[str] = None, order : int = 0):
    ''' 测试用例的批注

    name : 测试用例的名字
    
    dependencies : 依赖的测试用例
    
    order : 运行时的排序
    '''
    def decorator(fun):

        case_name = fun.__name__ if name is None else name

        if len(fun.__annotations__) > 0:
            system_utils.exit(f"{fun.__name__}方法不能添加方法参数")

        case_manager = CaseManager()
        case_manager.append_case(TestCase(
            fun=fun, 
            case_name=case_name, 
            dependencies=[dependencies] if type(dependencies) == str else dependencies, 
            order=order))

        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            case_manager.run_case(name, args, kwargs)
        return wrapper
    
    return decorator


if __name__ == "__main__":
    @test_case(name='1') 
    def first():
        print("1")

    @test_case(name='2', dependencies=["1"]) 
    def second():
        print("2")

    @test_case(name='3', dependencies="2") 
    def last():
        print("3")

    second()