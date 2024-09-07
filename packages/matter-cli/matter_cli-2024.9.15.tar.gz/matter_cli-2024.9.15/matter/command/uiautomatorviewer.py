# -*- encoding: utf-8 -*-
'''
@File		:	uiautomatorviewer.py
@Time		:	2024/02/19 16:37:02
@Author		:	dan
@Description:	自动下载sdkmanager，并且打开automatorviewer
'''

SDK_MANAGER_URL = 'https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip?hl=zh-cn'
# https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip?hl=zh-cn
# https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip?hl=zh-cn

import wget

if __name__ == '__main__':
    import sys
    sys.path.append('.')

from matter.utils.command import cmd, cmd_in_dir, is_install, cmd_with_content

from matter.utils.console import *
import matter.utils.system_utils as system_utils
from matter.utils.console import *
import pathlib
import zipfile
import os
import shutil
import platform
import tarfile
import subprocess


def java_version():
    '''
    获取java版本
    '''
    content = cmd_with_content('java', ['-version'])
    version = content[14:-1]
    version = version.split('_')[0]
    version = version.split('.')
    version = version[0] + '.' + version[1]
    return float(version)


def setup_java(dir) -> None:
    ''' 
    安装java
    '''

    urls : dict = {
        'x32':{
            'windows': 'OpenJDK11U-jdk_x86-32_windows_hotspot_11.0.22_7.zip',
        },
        'x64':{
            'windows': 'OpenJDK11U-jdk_x64_windows_hotspot_11.0.22_7.zip',
            'mac': 'OpenJDK11U-jdk_x64_mac_hotspot_11.0.22_7.tar.gz',
            'linux': 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz',
        }
    }
    mirror_url = 'https://mirrors.tuna.tsinghua.edu.cn/Adoptium'
    version = 11

    host_platform = platform.system().lower()
    if host_platform == 'darwin': 
        host_platform = 'mac'


    filename : str = urls['x64'][host_platform]
    url = f"{mirror_url}/{version}/jdk/x64/{host_platform}/{filename}"
    local_dir = f"{dir}/java/{filename}"
    out_path = f"{dir}/java/{version}/{host_platform}/"
    out_path = os.path.abspath(out_path)
    if not os.path.isdir(out_path):
        print_info(f'正在下载java，版本为{version}')
        p = pathlib.Path(local_dir)
        p = p.parent
        if not p.exists():
            p.mkdir(parents=True)
        try:
            wget.download(url, local_dir)
            print_info(f'下载java完成，开始解压')
        except:
            print_error(f'下载java失败，下载路径为{url}')
            return False
    


    if not os.path.isdir(out_path):
        try:
            if filename.endswith('.zip'):
                zip_file = zipfile.ZipFile(local_dir)
                zip_file.extractall(out_path)
                zip_file.close()
            else:
                tf = tarfile(local_dir)
                tf.extractall(out_path)
                tf.close()
            os.remove(local_dir)
            print_info(f'解压java成功，开始配置环境')
        except:
            print_error(f'解压java失败，解压目录为，{out_path}')
            return False
    

    p = pathlib.Path(out_path)
    for child in p.iterdir():
        out_path = child.absolute()
        break;
    
    try:
        if system_utils.is_windows():
            os.environ['JAVA_HOME'] = str(out_path);
            os.environ['PATH'] = "%JAVA_HOME%\\bin;" + str(os.environ['PATH']);
        else:
            os.environ['JAVA_HOME'] = str(out_path);
            os.environ['PATH'] = "$JAVA_HOME/bin:" + str(os.environ['PATH']);
        return True
    except Exception as ex:
        print(ex)
        print_error(f'java环境配置失败')
        return False

def setup(
        dir='matter_tools', 
        sdk_manager_version: str = '8512546') -> str | bool:
    ''' 下载sdkmanager
    
    Parameters
    ----------
    
    
    Returns
    -------
    None
    
    '''

    if not is_install('java') or java_version() <= 1.8:
        if not setup_java(dir):
            print_error(f'java环境失败')


    host_platform = platform.system().lower()
    if host_platform == 'windows':
        host_platform = 'win'
    elif host_platform == 'darwin':
        host_platform = 'mac'

    url = f"https://dl.google.com/android/repository/commandlinetools-{host_platform}-{sdk_manager_version}_latest.zip?hl=zh-cn"
    local_dir = f"{dir}/sdk_manager/commandlinetools-{host_platform}-{sdk_manager_version}_latest.zip"
    sdk_home = f"{dir}/sdk_manager/{sdk_manager_version}"
    out_path = f"{dir}/sdk_manager/{sdk_manager_version}_temp"
    sdk_home = os.path.abspath(sdk_home)
    if not os.path.isdir(sdk_home):
        print_info(f'正在下载sdk_manager，版本为{sdk_manager_version}')
        p = pathlib.Path(local_dir)
        p = p.parent
        if not p.exists():
            p.mkdir(parents=True)
        try:
            wget.download(url, local_dir)
            print_info(f'下载sdk_manager完成，开始解压')
        except:
            print_error(f'下载sdk_manager失败，下载路径为{url}')
            return False
    


    if not os.path.isdir(sdk_home):
        if os.path.isdir(out_path):
            shutil.rmtree(out_path, ignore_errors=True)

        try:
            zip_file = zipfile.ZipFile(local_dir)
            zip_file.extractall(out_path)
            zip_file.close()
            os.remove(local_dir)
            print_info(f'解压sdk_manager成功，开始配置环境')
        except:
            print_error(f'解压sdk_manager失败，解压目录为，{out_path}')
            return False
    
        def move_dir(src, dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)

            if os.path.isdir(src):
                shutil.copytree(src, dst)  
                shutil.rmtree(src)
            return
        p = pathlib.Path(out_path)
        for child in p.iterdir():
            out_path = child.absolute()
            break;
        out_path = pathlib.Path(out_path)
        cmdline_tools = pathlib.Path(f"{sdk_home}/cmdline-tools/latest")
        if not cmdline_tools.exists():
            cmdline_tools.mkdir(parents=True)
        move_dir(out_path.absolute(), cmdline_tools.absolute())

    if os.path.isdir(f'{sdk_home}/cmdline-tools') \
        and os.path.isdir(f'{sdk_home}/tools'):
        return sdk_home

    try:
        if system_utils.is_windows():
            auto_accept(f"{sdk_home}/cmdline-tools/latest/bin/sdkmanager.bat", ['--install', "emulator"])
            auto_accept(f"{sdk_home}/cmdline-tools/latest/bin/sdkmanager.bat", ['--install', "tools"])
            auto_accept(f"{sdk_home}/cmdline-tools/latest/bin/sdkmanager.bat", ['--install', "platform-tools"])
        
        else:
            cmd_in_dir(f"{sdk_home}/cmdline-tools/latest/bin", 'echo', ['y', '|', 'sdkmanager', '--install', "emulator"])
            cmd_in_dir(f"{sdk_home}/cmdline-tools/latest/bin", 'echo', ['y', '|', 'sdkmanager', '--install', "tools"])
            cmd_in_dir(f"{sdk_home}/cmdline-tools/latest/bin", 'echo', ['y', '|', 'sdkmanager', '--install', "platform-tools"])

        print_ok(f'sdk_manager环境配置成功')

    except Exception as ex:
        print(ex)
        print_error(f'sdk_manager环境安装失败')
        return False

    return sdk_home



def auto_accept(prog, args=[], license=True): 
    """
    自动输入yes
    """
    sub_args = args[:]
    sub_args.insert(0, prog)
    process = subprocess.Popen(args=sub_args, stdin=subprocess.PIPE, text=True)
    # for i in range(7):
    if license:
        output = process.communicate('y\ny\ny\n')
    else:
        output = process.communicate('y\n')


def run(args = None) -> None:
    ''' 
    自动打开安卓官方的 uiautomatorviewer.bat
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    matter_home = str(pathlib.Path.home().absolute()) + "/" + ".matter"
    sdk_home = setup(dir = matter_home)
    if sdk_home:
        if system_utils.is_windows():
            cmd(f'{sdk_home}/tools/bin/uiautomatorviewer.bat')
        else:
            cmd(f'{sdk_home}/tools/bin/uiautomatorviewer.sh')
        pass
    else:
        print_error("安装sdkmanager出错，你可以尝试重新输入")


if __name__ == '__main__':
    run()
