# -*- encoding: utf-8 -*-
'''
@File		:	console.py
@Time		:	2024/01/19 16:15:12
@Author		:	dan
@Description:	命令行输出封装
'''
    

def print_ok(text : str) -> None:
    ''' 输出绿色的文本
    
    Parameters
    ----------
    
    
    Returns
    -------
    None
    
    '''
    print(f"[OK]\t\t {text}" )
    


def print_info(text : str) -> None:
    ''' 输出白色的文本
    
    Parameters
    ----------
    
    
    Returns
    -------
    None
    
    '''
    print(f"[INFO]\t\t {text}" )

    


def print_warning(text : str) -> None:
    ''' 输出黄色的文本
    
    Parameters
    ----------
    
    
    Returns
    -------
    None
    
    '''
    print(f"[WARNING]\t {text}" )

def print_error(text : str) -> None:
    ''' 输出红色的文本
    
    Parameters
    ----------
    
    
    Returns
    -------
    None
    
    '''
    print(f"[ERROR]\t\t {text}" )


if __name__ == '__main__':
    print_info("开启测试")
    print_warning("含有警告")
    print_ok("测试通过")
    print_error("测试不通过")