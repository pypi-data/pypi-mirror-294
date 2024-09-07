import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    """自定义安装命令，允许用户通过 LTtx_tools_install 安装额外依赖"""
    def run(self):
        print("\n注意：要启用 pandas 相关功能，请运行 'LTtx_tools_install' 命令！\n")
        install.run(self)

def install_additional_tools():
    """通过这个方法来安装非必要依赖"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    else:
        print("找不到 requirements.txt 文件")

setup(
    name='LTtx',
    version='7.1.3',
    description='A Python wrapper for socket-based communication',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='95ge',
    author_email='445646258@qq.com',
    url='https://github.com/95ge/LTtx',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'LTtx_server=tx.LTtx_server:main',  # 定义入口点
            'LTtx_tools_install=tx.__init__:install_additional_tools',  # 自定义命令
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)
