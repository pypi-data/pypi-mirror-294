# -*- encoding: utf-8 -*-
'''
@File		:	browser.py
@Time		:	2024/01/05 09:47:49
@Author		:	dan
@Description:   浏览器的技术使用 selenium 实现，详情参考 https://www.selenium.dev/zh-cn/documentation/webdriver/getting_started/
'''

if __name__ == '__main__':
    import sys
    sys.path.append(".")
import os
import matter.utils.system_utils as system_utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, By
from selenium.webdriver.common.action_chains import ActionChains
import time

class BrowserEngine:
    '''
    浏览器引擎
    '''

    @property
    def driver_name(self) -> str:
        ''' 
        引擎名字
        '''
        
        return self.__driver_name

    @property
    def driver_path(self) -> str:
        ''' 
        本地路径
        '''
        return f"drivers/{self.driver_name}/{self.__version}/{self.driver_name}_driver.exe"
    
    @property
    def platform(self) -> str:
        ''' 
        操作系统
        '''
        return self.__platform
    
    @property
    def driver_url(self) -> str:
        ''' 
        下载路径
        '''
        return self.__driver_url.replace("#version#", self.__version)
    
    def __init__(self, platform, driver_name, driver_url, version) -> None:
        self.__platform = platform
        self.__driver_name = driver_name
        self.__driver_url : str = driver_url
        self.__version = version
        self.__arguments = None
        pass

    @property
    def arguments(self) -> list[str]:
        return self.__arguments
    
    @arguments.setter
    def arguments(self, value : list[str]):
        self.__arguments = value


    # 下载驱动，改用同步方法
    def driver(self) -> WebDriver:
        ''' 
        
        Parameters
        ----------
        
        
        Returns
        -------
        Driver
        
        '''
    
        if not os.path.isfile(self.driver_path):
            self.install()

        try:
            if self.driver_name == "chrome":
                option = webdriver.ChromeOptions()
                if self.__arguments:
                    for ar in self.__arguments:
                        option.add_argument(ar)
                service = webdriver.ChromeService(executable_path=self.driver_path)
                return webdriver.Chrome(options=option, service=service)
            if self.driver_name == "edge" or self.driver_name == "edge_x64":
                option = webdriver.EdgeOptions()
                if self.__arguments:
                    for ar in self.__arguments:
                        option.add_argument(ar)
                service = webdriver.EdgeService(executable_path=self.driver_path)
                return webdriver.Edge(options=option, service=service)
            if self.driver_name == "firefox" or self.driver_name == "firefox_x64":
                option = webdriver.FirefoxOptions()
                if self.__arguments:
                    for ar in self.__arguments:
                        option.add_argument(ar)
                service = webdriver.FirefoxService(executable_path=self.driver_path)
                return webdriver.Firefox(options=option, service=service)
            if self.driver_name == "explorer" or self.driver_name == "explorer_x64":
                option = webdriver.IeOptions()
                if self.__arguments:
                    for ar in self.__arguments:
                        option.add_argument(ar)
                option.add_argument("--no-sandbox")
                service = webdriver.IeService(executable_path=self.driver_path)
                return webdriver.Ie(options=option, service=service)
            if self.driver_name == "safari":
                option = webdriver.SafariOptions()
                if self.__arguments:
                    for ar in self.__arguments:
                        option.add_argument(ar)
                service = webdriver.SafariService(executable_path=self.driver_path)
                return webdriver.Safari(options=option, service=service)
        except Exception as msg:
            print("\n")
            print(msg)
            import re
            
            reg = "Current browser version is.+with"

            if not str(msg).__contains__("Current browser version"):
                system_utils.exit(f"该电脑不支持使用{self.driver_name}，请查看相关浏览器是否有安装。")
            version = re.search(reg, str(msg))\
                .group()\
                .replace("Current browser version is ", "")\
                .replace(" with", "")
            self.__version = version
            return self.driver()
            


    def install(self) -> bool:
        ''' 安装引擎
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool 安装是否成功
        
        '''
        import wget, zipfile, shutil, pathlib        

        zip_path = self.driver_path + ".zip"
        p = pathlib.Path(zip_path)
        p = p.parent
        if not p.exists():
            p.mkdir(parents=True)
        
        wget.download(self.driver_url, zip_path)
        zip_file = zipfile.ZipFile(zip_path)
        # 解压
        out_path = self.driver_path + ".out"
        zip_file.extractall(out_path)
        for f in os.listdir(out_path):
            if f.endswith(".exe"):
                shutil.copyfile(out_path + "/" + f, self.driver_path);
                break;
        zip_file.close()
        shutil.rmtree(out_path)
        os.remove(zip_path)
        

        return True


class Browser:

    ENGINES = {
        ## windows 平台
        "chrome"    : BrowserEngine("win", "chrome", "https://chromedriver.storage.googleapis.com/#version#/chromedriver_win32.zip", "114.0.5735.90"),
        "edge"      : BrowserEngine("win", "edge", "https://msedgedriver.azureedge.net/#version#/edgedriver_win32.zip", "120.0.2210.121"),
        "edge_x64"  : BrowserEngine("win", "edge_x64", "https://msedgedriver.azureedge.net/#version#/edgedriver_win64.zip", "120.0.2210.121"),
        "firefox"   : BrowserEngine("win", "firefox", "https://gonsin-common.oss-cn-shenzhen.aliyuncs.com/selenium_driver/geckodriver-#version#-win-aarch64.zip", "v0.34.0"),
        "firefox_x64"   : BrowserEngine("win", "firefox_x64", "https://gonsin-common.oss-cn-shenzhen.aliyuncs.com/selenium_driver/geckodriver-#version#-win-aarch64.zip", "v0.34.0"),
        "explorer"  : BrowserEngine("win", "explorer", "https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.14.0/IEDriverServer_Win32_#version#.zip", "4.14.0"),
        "explorer_x64": BrowserEngine("win", "explorer_x64", "https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.14.0/IEDriverServer_x64_#version#.zip", "4.14.0"),
        "safari"    : BrowserEngine("win", "safari", None, None),
    }

    @property
    def engine(self) -> BrowserEngine:
        return self.__engine
    
    @property
    def driver(self) -> WebDriver:
        return self.__driver
    
    def __init__(self, engine : str, url : str, window_size : str = "max", arguments:list = None) -> None:
        ''' 
        
        Parameters
        ----------
        engine : str : 浏览器引擎
        
        url : str : 浏览器第一次打开的路径

        window_size : str = "max" 窗口大小，格式为 1920x1080，或者max表示最大化
        
        arguments:list = selenium 内置参数

        '''
        
        self.__engine = Browser.ENGINES[engine];
        if self.__engine == None:
            system_utils.exit(f"不支持引擎 {engine}")
        self.__engine.arguments = arguments
        self.__window_size = window_size

        self.__url = url
        self.__opened = False
        self.__driver = None

        pass


    def init_driver(self) -> bool:
        ''' 初始化浏览器引擎
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool
        
        '''
        
        if self.__driver:
            return
        self.__driver = self.__engine.driver()
        


    def open(self) -> None:
        ''' 打开浏览器
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if self.__opened:
            return
        self.__opened = True
        if not self.__driver:
            self.init_driver()
            
        # 最大化浏览器
        if self.__window_size == 'max':
            self.__driver.maximize_window()
        else:
            width, height = self.__window_size.split("x")
            w = int(width)
            h = int(height)
            self.__driver.set_window_size(w, h)
        self.__driver.get(self.__url)
        time.sleep(1)


    def close(self) -> None:
        ''' 关闭浏览器
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            return
        self.__driver.close()
        self.__opened = False
        self.__driver = None
        pass

    def click(self, x, y) -> None:
        ''' 点击
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        ActionChains(self.driver).move_by_offset(x, y).click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()

    def slide(self, begin : tuple[2], end : tuple[2], speed : float = 200) -> None:
        ''' 点击
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        ActionChains(self.driver).move_by_offset(begin[0], begin[1]).click_and_hold()\
            .move_by_offset(end[0] - begin[0], end[1] - begin[1])\
            .release()\
            .perform()
        ActionChains(self.driver).move_by_offset(-end[0], -end[1]).perform()

    def double_click(self, x, y) -> None:
        ''' 左键双击
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        ActionChains(self.driver).move_by_offset(x, y).double_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()

    def context_click(self, x, y) -> None:
        ''' 右键单击
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        ActionChains(self.driver).move_by_offset(x, y).context_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()

    def get(self, url : str) -> None:
        ''' 打开指定路径
        
        Parameters
        ----------
        url : str ： 路径地址，格式为http://xxx.xxx.xx/ss
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        return self.driver.get(url)

    def click_xpath(self, xpath : str) -> None:
        ''' 根据xpath点击指定控件
        
        Parameters
        ----------
        url : str ： 路径地址，格式为http://xxx.xxx.xx/ss
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        self.driver.find_element(By.XPATH, xpath).click()

    def implicitly_wait(self, time : float) -> None:
        ''' 浏览器内等待一段时间
        
        Parameters
        ----------
        time : int ： 单位秒
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        self.driver.implicitly_wait(time_to_wait=time)

    def find_element(self, by : str, value : str) -> WebElement:
        ''' 查找浏览器的元素
        
        Parameters
        ----------
        by : str 根据 By 里面的定义
        
        value : str 
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        try:
            return self.driver.find_element(by, value)
        except Exception as ex:
            return None;


    def exist_element(self, by : str, value : str) -> None:
        ''' 查看某元素是否存在
        
        Parameters
        ----------
        by : int
        
        value : str
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        return self.driver.find_element(by, value) != None

    def click_by(self, by : str, value : str) -> None:
        ''' 点击某元素
        
        Parameters
        ----------
        by : int
        
        value : str
        
        Returns
        -------
        None
        
        '''
        if not self.__opened:
            self.open()
        self.find_element(by, value).click()


    def screenshot(self, image_path) -> None:
        ''' 
        
        Parameters
        ----------
        
        
        Returns
        -------
        str
        
        '''
        
        self.__driver.get_screenshot_as_file(image_path)


    def send_keys(self, text : str, element : WebElement = None) -> bool:
        ''' 输入文本
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool
        
        '''
        if not element:
            element = self.__driver.switch_to.active_element
            if not element:
                system_utils.exit('当前浏览器没有焦点')
        if not element:
            system_utils.exit('找不到需要输入的元素')
            return
        element.send_keys(text)


    def keyevent(self, key : str | int | tuple, element : WebElement = None) -> bool:
        ''' 输入文本
        
        Parameters
        ----------
        
        
        Returns
        -------
        bool
        
        '''
        if not element:
            element = self.__driver.switch_to.active_element
            if not element:
                system_utils.exit('当前浏览器没有焦点')
        if not element:
            system_utils.exit('找不到需要输入的元素')
            return
        element.send_keys(key)


if __name__ == '__main__':
    import time
    b = Browser("explorer", "http://www.baidu.com", "--no-sandbox")
    b.open()
    time.sleep(10);
    b.close()
