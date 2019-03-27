# @Time    : 2019/3/21 18:29
# @Author  : xufqing
#!/usr/bin/python
# -*- coding: utf-8 -*-

def _init():
    if not '_global_dict' in globals():
        global _global_dict
        _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue