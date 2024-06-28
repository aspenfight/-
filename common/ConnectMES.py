import requests
import json

from script.common.LogRecode import Logger
from script.common.SSHConnect import *

url = "https://sso.etron.cn:9006/api/"


def read_sn():
    ssh_handle = login_product('192.168.1.12', 'ubuntu')
    exp1 = execute_cmd_by_ssh(ssh_handle, 'cat pcba_sn.sn', prompt=['zu5'])
    if exp1 == 0:
        exp2 = execute_cmd_by_ssh(ssh_handle, 'ls -l', prompt=['factory_tools'])
        if exp2 == 0:
            return ssh_handle.before.decode('utf-8').split("\r\n")[3]


def get_boardinfo(sn, station):
    global log
    log = Logger(sn)
    if station == 'Program-1':
        station = 'burn1'
    elif station == 'FCT':
        station = 'FCT'
    elif station == 'IMU':
        station = 'chkbaidu'
    elif station == 'EOL':
        station = 'FCT1'
    params = {'ShellSerialNumber': sn, 'StationNumber': station}
    try:
        response = requests.get(url=url + 'GetAssySerialNumberMapping', params=params)
    except requests.exceptions.ConnectionError:
        log.logger.info("ERROR API Connection refused")
    else:
        # 获取请求状态码 200为正常
        if (response.status_code == 200):
            # 获取相应内容
            content = response.text
            # json转数组（Py叫字典，我喜欢叫数组）
            json_dict = json.loads(content)
            log.logger.info("Response from MES:")
            log.logger.info(json_dict)
            if (json_dict['ErrorCode'] == 0):
                sn_MES = json_dict['ShellSerialNumber']
                pn_MES = json_dict['PCBASerialNumbers']
                # 打印所有结果
                if station in ['Program', 'FCT']:
                    if sn_MES == sn:
                        log.print_log("sn check ok")
                        return 'ok'
                    else:
                        return 'SN Not Same'
                else:
                    board_sn = read_sn()
                    if board_sn == sn_MES:
                        log.print_log("sn check ok")
                        return 'ok'
                    else:
                        return 'SN Not Same'
            else:
                log.logger.info(json_dict['ErrorMessage'])
                return json_dict['ErrorMessage']
        else:
            log.logger.info("Requst Fail!")
            return "Requst Fail!"


def check_boardinfo(sn, station):
    global log
    log = Logger(sn)
    if station == 'Program-1':
        station = 'burn1'
    elif station == 'FCT':
        station = 'FCT'
    elif station == 'IMU':
        station = 'chkbaidu'
    elif station == 'EOL':
        station = 'FCT1'
    # requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    # s = requests.session()
    # s.keep_alive = False  # 关闭多余连接
    params = {'SerialNumber': sn, 'StationNumber': station}
    try:
        response = requests.get(url=url + 'CheckSerialNumberState', params=params)
    except requests.exceptions.ConnectionError:
        log.logger.info("ERROR API Connection refused")
        return "Requst Fail!"
    else:
        # 获取请求状态码 200为正常
        if (response.status_code == 200):
            # 获取相应内容
            content = response.text
            # json转数组（Py叫字典，我喜欢叫数组）
            json_dict = json.loads(content)
            log.logger.info("Response from MES:")
            log.logger.info(json_dict)
            if (json_dict['ErrorCode'] == 0):
                log.print_log("sn check ok")
                return 'ok'
            else:
                log.logger.info(json_dict['ErrorMessage'])
                return json_dict['ErrorMessage']
        else:
            log.logger.info("Requst Fail!")
            return "Requst Fail!"



def uploadState(sn, station, result, DefectCode):
    global log
    log = Logger(sn)
    params = {'SerialNumber': sn, 'StationNumber': station, 'Result': result, 'DefectCode': DefectCode}
    try:
        response = requests.get(url=url + 'CheckSerialNumberState', params=params)
    except requests.exceptions.ConnectionError:
        log.logger.info("ERROR API Connection refused")
        return "Requst Fail!"
    else:
        # 获取请求状态码 200为正常
        if response.status_code == 200:
            # 获取相应内容
            content = response.text
            # json转数组
            json_dict = json.loads(content)
            log.logger.info("Response from MES:")
            log.logger.info(json_dict)
            if json_dict['ErrorCode'] == 0:
                log.print_log("uploadState ok")
                return 'ok'
            else:
                log.logger.info(json_dict['ErrorMessage'])
                return json_dict['ErrorMessage']
        else:
            log.logger.info("Requst Fail!")
            return "Requst Fail!"


def uploadLogToMES(sn, station, result, CustomerName, ProductModel, LogFilePath):
    with open(LogFilePath, "rb") as f:
        LogFileStream = f.read()
    data_json = json.dumps(
        {'SerialNumber': sn, 'StationNumber': station, 'TestingResult': result, 'CustomerName': CustomerName,
         'ProductModel': ProductModel, 'LogFileStream': LogFileStream})  # dumps：将python对象解码为json数据
    r_json = requests.post(url + 'UploadLogToMES', data=data_json)
    print(r_json)
    print(r_json.text)
    print(r_json.content)
