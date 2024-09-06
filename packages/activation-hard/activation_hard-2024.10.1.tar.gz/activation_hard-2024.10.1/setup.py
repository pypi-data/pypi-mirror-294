# coding: utf-8
import os,shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        # 这里加入我们要执行的代码
        install.run(self)

setup(
    name='activation-hard',  # 包名
    version='2024.10.1',  # 版本号
    cmdclass={
        'install': PostInstallCommand,
    },
    description='权限激活相关',
    long_description='',
    author='tencent',
    author_email='pengluan@tencent.com',
    url='https://github.com/data-infra/cube-studio',
    license='',
    install_requires=[
        'PySnooper',
        'kubernetes',
        "cryptography"
    ],
    python_requires='>=3.6',
    keywords='',
    packages=find_packages("src"),  # 必填 包含所有的py文件
    package_dir={'': 'src'},  # 必填 包的地址
    include_package_data=True,  # 将数据文件也打包
    )
