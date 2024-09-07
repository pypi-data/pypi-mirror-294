# -*- encoding: utf-8 -*-
'''
@File		:	matter_command.py
@Time		:	2024/01/05 10:26:11
@Author		:	dan
@Description:	matter 命令行入口

matter proxy -p [port]    
开启代理服务器，监听来自远端测试脚本的命令


'''

import sys
if __name__ == '__main__':
    sys.path.append('.')
import argparse
import matter.command.run_proxy as run_proxy_accept
import matter.command.record as record_accept
import matter.command.run_accept as run_accept
import matter.command.uiautomatorviewer as uiautomatorviewer_accept

import click


def main():
    try:
        result = run()
        sys.exit(result)
    except Exception as e:
        print(e)
        sys.exit(-1)


def run(args : None):
    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser("matter", add_help=False)
    subparsers = parser.add_subparsers(title='以下是matter提供工具', metavar='command')
    run_proxy_parser = subparsers.add_parser('run_proxy', help="开启代理服务器")
    run_proxy_parser.set_defaults(handle=run_proxy_accept.run)

    run_parser = subparsers.add_parser('run', help="运行 matter 测试用例")
    run_parser.set_defaults(handle=run_accept.run)

    uiauto_parser = subparsers.add_parser('uiautomatorviewer', help="打开uiautomatorviewer")
    uiauto_parser.set_defaults(handle=uiautomatorviewer_accept.run)

    record_parser = subparsers.add_parser('record', help="运行脚本录制管理器")
    record_parser.set_defaults(handle=record_accept.run)

    parser.add_argument('-h', '--help', help='查看帮助', required=False, default=False, action="store_true")
    parser.add_argument('-v', '--version', help='查看版本', required=False, default=False, action="store_true")

    
    result = parser.parse_args(args[0:1])

    if hasattr(result, 'handle'):
        return result.handle(args[1:])
    

    if result.help:
        parser.print_help()
        return 0;
    if result.version:
        print("1.0")
        return 0;
    parser.print_help()
    return 0



# @click.group()
# @click.option('-d', '--debug', default=False, help='显示更多日志（用于调试）')
# @click.option('-h', '--help', default=False, help='查看帮助')
# @click.pass_context
# def main(ctx, debug, help):
#     ctx.ensure_object(dict)
#     ctx.obj['DEBUG'] = debug
#     ctx.obj['help'] = help

# @main.command(name = "uiautomatorviewer", help="打开uiautomatorviewer")
# @click.pass_context
# def uiautomatorviewer_command(ctx):
#     print(ctx)

# @main.command(name = "run", help="运行 matter 测试用例")
# def run_command(ctx):
#     print(ctx)

# @main.command(name = "record", help="运行脚本录制管理器")
# def record_command(ctx):
#     print(ctx)

# @main.command(name = "run_proxy", help="运行代理")
# @click.option('-p', '--port', help='指定监听端口端口')
# @click.pass_context
# def run_proxy_command(ctx):
#     print(ctx)

if __name__ == '__main__':
    try:
        args = [];
        # args.append("uiautomatorviewer")
        # args.append("-h")
        args.append("run_proxy")
        args.append("-h")
        result = run(args)
        sys.exit(result)
    except Exception as e:
        print(e)
        sys.exit(-1)


