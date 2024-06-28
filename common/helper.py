import os
from common.Configer import *


class CommonHelper:
    def __init__(self):
        pass
    @staticmethod
    def readQss(style):
        with open(style,"rb") as f:
            return f.read().decode('gbk')


def config(filepath,section='General',option='',value='nan'):
    configHandle.read(filepath, encoding='GB18030')
    if value == 'nan':
        res = configHandle.get(section, option)
        if res.lower() == 'true':
            return True
        elif res.lower() == 'false':
            return False
        else:
            return res
    else:
        res = configHandle.set(section, option, str(value))
        configHandle.write(open(filepath,'w'))
    return res

def get_config_items(filepath,section='General'):
    configHandle.read(filepath, encoding='GB18030')
    return configHandle.items(section)

def makeDir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False