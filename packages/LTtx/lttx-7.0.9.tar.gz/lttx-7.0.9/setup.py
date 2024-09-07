from setuptools import setup, find_packages

setup(
    name='LTtx',
    version='7.0.9',
    description='天行量化通信组件，适合用在分布式的网络通信组件，若要使用全部功能，确保安装了pandas库',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='txquant',
    author_email='445646258@qq.com',
    url='https://github.com/95ge/LTtx',
    license='MIT',
    packages=find_packages(),  # 自动查找并包含包
    include_package_data=True,  # 包括包内的其他文件
    package_data={
        'tx': ['Config.txt'],  # 指定需要打包的额外文件
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
        'pandas_market_calendars',
        'pyzmq',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'LTtx_server=tx.LTtx_server:main',  # 定义入口点
        ],
    },
)
