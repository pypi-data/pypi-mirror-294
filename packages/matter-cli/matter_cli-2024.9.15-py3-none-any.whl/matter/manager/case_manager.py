# -*- encoding: utf-8 -*-
'''
@File		:	case_manager.py
@Time		:	2024/01/11 16:23:01
@Author		:	dan
@Description:	测试用例管理类，管理着项目中所有的测试用例的依赖关系

依赖的原则：
    1. 必须是单方向，在前头的不能依赖在后头的测试用例
    2. 一个测试用例可以被多个测试用例依赖，一个测试用例可以依赖多个测试用例，即多对多关系
    3. 运行顺序，最底层的依赖先运行，如果是同一级别，则根据order排序，order越高越先运行，如果order相同，则按照排列顺序执行
'''


import functools
from typing import Any

from matter.utils.singleton import singleton
import matter.utils.system_utils as system_utils


class TestCase:
    ''' 
    测试用例类
    '''
    @property
    def fun(self):
        return self.__fun

    @property
    def case_name(self) -> str:
        return self.__case_name

    @property
    def dependencies(self) -> list:
        return self.__dependencies

    @property
    def order(self) -> int:
        return self.__order

    @property
    def level(self) -> int:
        return self.__level
    
    @property
    def annotations(self):
        return self.__annotations
    

    def __init__(self, fun : any, case_name : str, dependencies : list[str] = [], order : int = 0) -> None:
        ''' 
        
        Parameters
        ----------
        callable : any 测试用例的方法
        
        case_name : str 用例的名字
        
        dependencies : list[str] = [] 依赖的用例
        
        order : int = 0 排序
        
        '''
        self.__fun = fun
        self.__case_name = case_name
        self.__dependencies = dependencies
        self.__order = order
        self.__level = 0;
        self.__annotations = fun.__annotations__
        
        pass
    
    def __hash__(self) -> int:
        return hash(self.case_name)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        # return self.__fun(args, kwds)
        self.__fun
        return self.__fun()
    
    def __str__(self) -> str:
        return self.__case_name

    def __eq__(self, __value: object) -> bool:
        if not __value:
            return False
        
        if not isinstance(__value, TestCase):
            return False
        
        return self.__case_name.__eq__(__value.__case_name)
    

@singleton
class CaseManager:
    '''
    测试用例管理类，管理着项目中所有的测试用例的依赖关系
    '''
    def __init__(self) -> None:
        self.__cases : dict[str, TestCase] = {}


    def append_case(self, test_case : TestCase) -> None:
        ''' 添加测试用例
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if self.__cases.__contains__(test_case.case_name):
            system_utils.exit(f'测试用例名字不能重复，名字为{test_case.case_name}')

        self.__cases[test_case.case_name] = test_case

    def run_case(self, case_name : str, *args, **kwargs) -> None:
        ''' 运行测试用例
        
        Parameters
        ----------
        case_name 测试用例的名字
        
        Returns
        -------
        None
        
        '''
        need_run : list[TestCase] = self.__need_run(case_name, [])
        need_run : set[TestCase] = set(need_run)
        need_run = self.sort_by_level_and_order(list(need_run))
        for case in need_run:
            case(args, kwargs);
    
    def sort_by_level_and_order(self, cases : list[TestCase]) -> list[TestCase]:
        ''' 根据被依赖数 和 order进行排序
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        case_sorted : list[TestCase] = []
        max_loop = len(cases)
        i = 0
        while cases and i < max_loop:
            for case in cases:
                if not case.dependencies:
                    case_sorted.append(case)
                    cases.remove(case)
                    continue;

                all_use = True
                for dep in case.dependencies:
                    dep_case = self.__cases[dep]
                    if not case_sorted.__contains__(dep_case):
                        all_use = False
                        break;
                if all_use:
                    case_sorted.append(case)
                    cases.remove(case)
            i += 1

        ## 如果循环结束，还有剩余的没有加入到case_sorted ，表示测试用例的依赖树中有循环。
        if len(cases) > 0:
            case_in_loop = []
            for case in cases:
                case_in_loop.append(case.case_name)
            case_in_loop = ", ".join(case_in_loop)
            system_utils.exit(f"以下测试用例发现了依赖循环：\n {case_in_loop}")
        return case_sorted;


    def find_case(self, case_name : str) -> TestCase:
        ''' 查询测试用例
        
        Parameters
        ----------
        case_name : str 测试用例的名字
        
        Returns
        -------
        TestCase
        
        '''
        test_case = self.__cases.get(case_name)
        if not test_case:
            system_utils.exit(f'查找不到测试用例{case_name}，请查看yml文件是否书写正确')
        return self.__cases[case_name]


    def sub_list(self, l1 : list, l2 : list) -> list:
        ''' 2个列表相减
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        temp = list(l1)
        for i in l2:
            if l1.__contains__(i):
                temp.remove(i)

        return temp        
    
    def __need_run(self, case_name : str, need_run : list[TestCase] = []) -> list[TestCase]:
        ''' 列出所有需要运行的测试用例
        
        Parameters
        ----------
        
        
        Returns
        -------
        list[TestCase]
        
        '''

        case = self.__cases[case_name]
        if need_run.__contains__(case):
            system_utils.exit(f"测试用例 {case.case_name} 发生依赖循环")
        need_run.append(case)
        if case.dependencies:
            for dep in case.dependencies:
                sub_need_run = list(need_run)
                sub_need_run = self.__need_run(dep, sub_need_run)
                need_run.extend(sub_need_run)
                    
        return need_run
        

    
        