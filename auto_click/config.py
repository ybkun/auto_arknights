#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/12/12 21:15 
# @Author : ybkun 
# @File : config.py 
# @Software: PyCharm


import os
import json

_cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_cur_dir, "config.json"), 'r', encoding='utf-8') as fid:
    config = json.load(fid)

adb_exe = os.path.abspath(config['adb_exe'])

print(adb_exe)
