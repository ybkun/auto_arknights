#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 20:28 
# @Author : ybkun 
# @File : img_tools.py 
# @Software: PyCharm

__all__ = ['Position', 'find_center']

import cv2
import numpy
from typing import Optional


class Position(object):
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_pair(self):
        return self.x, self.y


def find_center(screen_file: str, img_template: numpy.ndarray) -> Optional[Position]:
    img_screen = cv2.imread(screen_file)
    tmp_height, tem_width = img_template.shape[:2]
    match_result = cv2.matchTemplate(img_screen, img_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
    if max_val < 0.98:
        return None
    return Position(max_loc[0] + tem_width / 2, max_loc[1] + tmp_height / 2)
