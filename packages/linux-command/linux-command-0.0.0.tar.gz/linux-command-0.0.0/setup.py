from setuptools import setup, find_packages

setup(
    name='linux-command',  # 包名
    version='0.0.0',   # 版本号
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cmd=linux_command.linux_command:main',  # 定义命令行工具
        ],
    },
    install_requires=[],  # 依赖的包，如果有的话
    author='Mouxiao Huang',
    author_email='huangmouxiao@gmail.com',  # 作者邮箱
    description='A command line tool to perform custom tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mycommand',  # 项目地址，假设托管在 GitHub 上
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
