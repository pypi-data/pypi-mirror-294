# -*- coding: utf-8 -*-
# @Project: MangoActuator
# @Description: 
# @Time   : 2023-07-07 10:14
# @Author : 毛鹏


class TestKitError(Exception):

    def __init__(self, code: int, msg: str, value: tuple = None, error: str = None, is_log=True):
        if value:
            msg = msg.format(*value)
        if error and is_log:
            pass
        else:
            pass
        self.code = code
        self.msg = msg
