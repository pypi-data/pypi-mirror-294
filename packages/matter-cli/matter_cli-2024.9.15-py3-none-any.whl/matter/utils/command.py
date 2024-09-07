


import subprocess
import os
import platform
import sys




def host_platform():
  """
  查看操作系统类型，返回内容： mac/linux/win32/win64
  """
  ret = platform.system().lower()
  if (ret == "darwin"):
    return "mac"
  return ret

def is_windows():
  """
  是否是windows操作系统
  """
  if "windows" == host_platform():
    return True
  return False


def get_path(path):
  """
  归一化路径，如果是windows平台，将/转化为\\
  """
  if "windows" == host_platform():
    return path.replace("/", "\\")
  return path

def cmd(prog, args=[], is_no_errors=False): 
  """
  运行命令行，并返回操作结果（0表示成功，其他表示错误）
  """
  ret = 0
  if ("windows" == host_platform()):
    sub_args = args[:]
    sub_args.insert(0, get_path(prog))
    ret = subprocess.call(sub_args, stderr=subprocess.STDOUT, shell=True)


  else:
    command = prog
    for arg in args:
      command += (" \"" + arg + "\"")
    if not is_root():
      command = "sudo " + command
    ret = subprocess.call(command, stderr=subprocess.STDOUT, shell=True)
  if ret != 0 and not is_no_errors:
    sys.exit("Error (" + prog + "): " + str(ret))
  return ret



def cmd_with_content(prog, args=[]):  
  """
  运行命令行，并返回 命令行内容
  """
  ret = ""
  if ("windows" == host_platform()):
    sub_args : list = args[:]
    sub_args.insert(0, get_path(prog))
    ret = subprocess.getoutput(sub_args)
  else:
    command = prog
    for arg in args:
      command += (" \"" + arg + "\"")
    if not is_root():
      command = "sudo " + command
    ret = subprocess.getoutput(command)
  return ret


def cmd_in_dir(directory, prog, args=[], is_no_errors=False):
  """
  在指定目录里运行命令
  """
  dir = get_path(directory)
  cur_dir = os.getcwd()
  os.chdir(dir)
  next_dir = os.getcwd()
  if prog.endswith(".sh"):
    cmd("chmod", ["777", prog])
  ret = cmd(prog, args, is_no_errors)
  os.chdir(cur_dir)
  return ret




def is_install(shell) -> bool:
  ''' 查看是否存在某个命令行
  
  Parameters
  ----------
  
  
  Returns
  -------
  bool
  
  '''
  
  if cmd(shell, ['-v'], True) == 0:
    return True;
  
  if cmd(shell, ['--version'], True) == 0:
    return True;
  
  if cmd(shell, ['-version'], True) == 0:
    return True;

  return False


def is_root():
  """
  判断当前是否为root账号
  """
  if is_windows():
    return False
  return os.geteuid() == 0;