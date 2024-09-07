# tx/__init__.py

from .tx import txl
import os
import subprocess
import sys

def install_additional_tools():
    """自定义命令函数，用户可以通过 'LTtx_tools_install' 安装非必要依赖"""
    requirements_file = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    if os.path.exists(requirements_file):
        print("正在安装额外依赖...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    else:
        print("找不到 requirements.txt 文件，请检查路径。")
