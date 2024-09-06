# -*- coding: utf-8 -*-
"""
@author:lpf
@file: setup.py
@time: 2024/9/6  13:52
"""
import setuptools

# 导入静态文件
file_data = [
    "README.md",
]
# 自动读取readme
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
setuptools.setup(
    name="biggai",  # Replace with your own username
    version="0.1.0",
    author="lpf_andr",
    author_email="lpf_andr@163.com",
    description="A feishu api package for django",
    readme="README.md",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitee.com/li-pf/django_feishu_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    data_files=file_data,  # 打包时需要打包的数据文件，如图片，配置文件等
    packages=setuptools.find_packages(),
    install_requires=['cryptography', 'pydantic', 'aiohttp', 'requests', 'pycryptodome'],  # 安装所需要的库
)
