#!/usr/bin/python
# -*- coding: utf-8 -*-
# 本方法用于跨PY脚本进行变量传输
def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
