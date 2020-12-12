#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/12/11 21:13 
# @Author : ybkun 
# @File : run_ak_prepared.py
# @Software: PyCharm

"""
预先准备好要刷的图
然后开始执行
"""

import os
import cv2
import numpy
import time
from log_utils import get_logger
from auto_click.adb_tools import *
from auto_click.img_tools import *

cur_dir = os.path.dirname(os.path.abspath(__file__))
img_tpl_dir = os.path.join(cur_dir, "img_tpl")

img_action_1 = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_start_action_1.png"))
img_action_2 = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_start_action_2.png"))
img_acting = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_take_over.png"))
img_finished = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_reliability_up.png"))
img_recover_page_medicine = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_recover_page_medicine.png"))
img_recover_page_confirm = cv2.imread(os.path.join(img_tpl_dir, "tpl_ak_recover_page_confirm.png"))

__screenshot_file = "screen.png"

logger = get_logger("run_ak_prepared")


def save_screenshot():
    take_screenshot(__screenshot_file)


def wait(second):
    time.sleep(second)


def get_position_pair(img_template: numpy.ndarray):
    save_screenshot()
    position = find_center(__screenshot_file, img_template)
    if not position:
        logger.error("图像不匹配，异常终止")
        exit(1)
    return position.get_pair()


def try_action_1():
    click(get_position_pair(img_action_1))
    wait(2)


def try_action_2():
    click(get_position_pair(img_action_2))


def try_end():
    click(get_position_pair(img_finished))


def is_acting() -> bool:
    save_screenshot()
    if find_center(__screenshot_file, img_acting):
        return True
    return False


def is_medicine_page() -> bool:
    """
    是否出现理智恢复页面
    限制使用合剂
    """
    save_screenshot()
    if find_center(__screenshot_file, img_recover_page_medicine):
        return True
    return False


def try_take_medicine():
    click(get_position_pair(img_recover_page_confirm))
    wait(2)


class RestMedicineCounter(object):
    __slots__ = ['value']

    def __init__(self, max_count: int = 3):
        self.value = max_count

    def sub(self):
        if self.value > 0:
            self.value -= 1

    def ok(self) -> bool:
        return self.value != 0

    def __repr__(self):
        return f"<RestMedicineCounter value={self.value}>"

    def __str__(self):
        return self.__repr__()


def run_one_round(main_wait_second: int, rest_medicine_counter: RestMedicineCounter = RestMedicineCounter(-1)):
    """
    刷一轮
    :param main_wait_second: 作战时常
    :param rest_medicine_counter: 剩余可用理智提升次数，小于0则不限制
    """
    try_action_1()
    if is_medicine_page():
        if rest_medicine_counter.ok():
            rest_medicine_counter.sub()
            try_take_medicine()
            logger.info(f"已使用合剂恢复理智，剩余{rest_medicine_counter.value}次")
            try_action_1()
        else:
            logger.warning(f"剩余理智恢复次数={rest_medicine_counter.value}，退出")
            exit(1)
    logger.info("已进入行动配置页")
    try_action_2()
    logger.info("开始行动")
    wait(main_wait_second)
    while is_acting():
        wait(10)
    logger.info("行动已结束")
    wait(3)
    try_end()
    logger.info("已返回地图")


def run(main_wait_second: int = 3 * 60, max_round: int = 100, rest_medicine_count: int = 0):
    """
    循环刷
    :param main_wait_second: 作战时常
    :param max_round: 最多刷几轮
    :param rest_medicine_count: 最多使用几次合剂
    """
    count = 0
    rest_medicine_counter = RestMedicineCounter(rest_medicine_count)
    while count < max_round + 1:
        count += 1
        logger.info(f"round {count} start")
        run_one_round(main_wait_second, rest_medicine_counter)
        logger.info(f"round {count} end")
        wait(5)
    logger.info(f"完成预定的{max_round}轮操作，正常终止")


if __name__ == '__main__':
    run(140, rest_medicine_count=1)
