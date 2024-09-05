# -*- coding: utf-8 -*-
"""
@ Created on 2024-09-04 17:00
---------
@summary: 
---------
@author: XiaoBai
"""
from sys import version_info

import setuptools

if version_info < (3, 6, 0):
    raise SystemExit("Sorry! geocoding requires python 3.6.0 or later.")

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
packages.extend(
    [
        "geocoding",
    ]
)

requires = [
    "jieba>=0.42.1",
    "pandas>=1.5.3"
]

setuptools.setup(
    name="pygeocoding",
    version="1.1.1",
    author="XiaoBai",
    license="MIT",
    author_email="1808269437@qq.com",
    python_requires=">=3.6",
    description="地址标准化工具",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
