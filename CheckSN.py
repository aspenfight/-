import time
from common.LogRecode import *
from common.MysqlHandle import *
import common.globalvar as gl
from common.LogRecode import *
import traceback

isRunning = config(pathRunConfig, option='IsRunning')
gl._init()
if not isRunning:
    gl.set_value('DEBUG', True)
else:
    gl.set_value('DEBUG', False)


def CheckStation(params):
    print("check station Start")
    print(params)
    return 'ok'
    sn = params[0]
    station = params[1]
    if station.lower() == 'burnins':
        table = 'recode_si'
    client = HandleMysql()
    sql = "select * from " + table + " where sn='{}' and result='OK' order by id desc".format(sn)
    print(sql)
    res = client.query_sql(sql)
    print(res)
    if res is None:
        print('此产品与当前站位不匹配')
        return 'fail'
    else:
        print('已测到到相关数据')
        return 'ok'

def UploadRecodeToMES(params):
    try:
        create_log_debug(params)
        print_system_log(params)
        sn = params[0]
        station = params[1]
        # table = f'gabbo_{station.lower()}'
        table = "dc_board"
        result = params[2]
        if result == 0:
            test_result = 'OK'
        else:
            test_result = 'NG'

        client = HandleMysql()
        # sql = "select * from "+table+" where SerialNumber='{}'".format(sn)
        # print_system_log(sql)
        # res = client.query_sql(sql)
        # print_system_log(res)
        timestamp = int(time.time())
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        sql = ["insert into " + table + " (SerialNumber,TestResult,TestDate) values ('{}','{}','{}')".format(sn,
                                                                                                             test_result,
                                                                                                             t)]

        # if res is None:
        #     sql = ["insert into "+table+" (sn,result,date) values ('{}','{}','{}')".format(sn,result,t)]
        # else:
        #     sn = res['SerialNumber']
        #     sql = [
        #         "update "+table+" set result='{}',date='{}' where id = '{}'".format(test_result, t,sn)]
        print_system_log(sql)
        result = client.execute(sql)
        print_system_log(result)
        if result is None:
            return 'ok'
    except Exception as e:
        print_system_log(traceback.format_exc())
        return 'fail'

def CheckOut(params):
    return {'code':1,'msg':'ok'}

# 串口超时是最大的等待时间
def main():
    sn = '123456789'
    mac = '54:ef:fe:20:04:eb'
    result='fail'
    pn = '800-0004'
    # upload_data(sn,mac,result)
    UploadRecodeToMES(['1','OK','1'])



if __name__ == '__main__':
    main()
