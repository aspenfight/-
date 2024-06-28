import logging
from logging import handlers
import os
import sys
import common.globalvar as gl
import datetime

class Logger():
    # 获取当前的文件路径
    # log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(os.path.dirname("C:\\ProgramData\\Cabbage\\System log\\Buffer\\"))
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, sn, level='debug', when='D', backCount=3,
                 fmt='%(asctime)s : %(message)s'):
        if sn == '':
            return
        self.file_name = '\\' + str(sn) + '.log'
        print('日志的存储路径：' + self.log_path + self.file_name)
        self.logger = logging.getLogger(name=self.file_name)
        # 日志重复打印 [ 判断是否已经有这个对象，有的话，就再重新添加]
        if not self.logger.handlers:
            # if level.lower() == "critical":
            #    self.logger.setLevel(logging.CRITICAL)
            # elif level.lower() == "error":
            #    self.logger.setLevel(logging.ERROR)
            # elif level.lower() == "warning":
            #    self.logger.setLevel(logging.WARNING)
            # elif level.lower() == "info":
            #    self.logger.setLevel(logging.INFO)
            # elif level.lower() == "debug":
            #    self.logger.setLevel(logging.DEBUG)
            # else:
            #    self.logger.setLevel(logging.NOTSET)
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)

            format_str = logging.Formatter(fmt)  # 设置日志格式
            self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            th = handlers.TimedRotatingFileHandler(filename=self.log_path + self.file_name, when=when,
                                                   backupCount=backCount,
                                                   encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            th.setFormatter(format_str)  # 设置文件里写入的格式
            self.logger.addHandler(sh)  # 把对象加到logger里
            self.logger.addHandler(th)

    def __del__(self):
        # self.logger.removeHandler(self.sh)
        # self.logger.removeHandler(self.th)
        logging.shutdown()

    def print_log(self, message):
        self.logger.info('*' * 30 + message + '*' * 30)


def create_log_debug(param):
    DEBUG = gl.get_value('DEBUG')
    if DEBUG:
        log = Logger('debug')
        gl.set_value('log', log)
    else:
        if len(param) >= 2:
            gl.set_value('log', param[-2])
            gl.set_value('debug', param[-1])
        else:
            print('*' * 30)
            print('*请关闭主程序框架后再进行调试*')
            print('*' * 30)
            exit()


def print_system_log(string,style=1):
    log = gl.get_value('log')
    debug = gl.get_value('debug')
    if style == 2:
        string = '*'*30+string+'*'*30

    # current_date_time = QDateTime.currentDateTime().toString("MM-dd hh:mm:ss:zzz")
    now = datetime.datetime.now()
    # str(now)[5:-3]
    current_date = ("{}").format(str(now)[5:-3])
    message = ("[{}] {} ").format(current_date, string)
    if debug:
        try:
            debug.EmitAppendSig(message)
        except AttributeError:
            print('*' * 30)
            print('*请关闭主程序框架后再进行调试*')
            print('*' * 30)
            exit()
    log.logger.info(string)
