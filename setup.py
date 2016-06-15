#!/usr/bin/env python
# coding=utf-8

import sys
if sys.version_info[0] != 2 or sys.version_info[1] < 7:
    sys.exit('Sorry, Python = 2.7 is not supported')

from setuptools import setup, find_packages
setup(
        name = 'qcloud_cos',
        version = '3.3',
        description = 'python sdk for tencent qcloud cos',
        license = 'MIT License',
        install_requires=['requests'],

        author = 'chengwu',
        author_email = 'chengwu@tencent.com',

        packages = find_packages(),
        )
