#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 20:22 
# @Author : ybkun 
# @File : adb_tools.py
# @Software: PyCharm

__all__ = ['take_screenshot', 'pull_file', 'push_file', 'click']

import os
from .config import adb_exe

__adb_executable = adb_exe


def take_screenshot(out_file: str):
    os.system(f"{__adb_executable} shell screencap -p /data/screenshot.png")
    os.system(f"{__adb_executable} pull /data/screenshot.png {out_file}")


def pull_file(src_file: str, out_file: str):
    os.system(f"{__adb_executable} pull {src_file} {out_file}")


def push_file(outer_file: str, inner_file: str):
    os.system(f"{__adb_executable} push {outer_file} {inner_file}")


def click(center, offset=(0, 0)):
    (x, y) = center
    x += offset[0]
    y += offset[1]
    os.system(f"{__adb_executable} shell input tap {x} {y}")
