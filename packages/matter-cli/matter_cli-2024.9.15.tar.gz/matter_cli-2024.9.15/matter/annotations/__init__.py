# -*- encoding: utf-8 -*-
'''
@File		:	__init__.py
@Time		:	2024/01/11 16:23:07
@Author		:	dan
@Description:	@test_case 批注的实现，用@test_case 定义一个测试用例
'''


import functools

def test_case(name : str, dependencies : str | list[str] = None):
    ''' 测试用例的批注

    name : 测试用例的名字
    
    dependencies : 依赖的测试用例，被依赖的测试用例会优先执行
    '''

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # print(f"Decorator argument: {name}")
            return f(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    @test_case(name='1') 
    def first():
        print("1")

    @test_case(name='2', dependencies="1") 
    def second():
        print("2")

    @test_case(name='3', dependencies="2") 
    def last():
        print("3")

    last()