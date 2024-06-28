import pyvisa as visa
import sys
import time
import common.globalvar as gl
from common.LogRecode import *


# visa.log_to_screen()


# inter_loc = sys.argv[1]
# command = sys.argv[2]

def e2float(value):
    ss = value.split("\n")[0]
    ss = ss.replace("\n", "")
    k = float(ss)
    if k<0.001:
        k = round(k, 6)
    else:
        k = round(k, 3)
    # print(str(k))
    return str(k)


def create_visaobj(address):
    visaObj = visa.ResourceManager()
    try:
        obj = visaObj.open_resource(address)
        return obj
    except Exception as e:
        print(e)


# 查看设备列表
def get_manege_list():
    print_system_log('获取设备列表')
    visaObj = visa.ResourceManager()
    managelist = visaObj.list_resources()
    print(managelist)
    return managelist


def get_details(address):
    print_system_log('运行命令>>>>>*IDN?')
    result = send_commend_query(address, '*IDN?')
    return result


def get_current_for_battery(address):
    inst = create_visaobj(address)
    command = ":MEAS2:CURR?"
    res = inst.query(command)
    print_system_log(res)
    curr = e2float(res)
    return curr

def get_current(address):
    print_system_log("MEAS current")
    inst = create_visaobj(address)
    res = inst.query(':MEAS:CURR?')
    result = e2float(res)
    print_system_log(result)
    return result


def get_volt(address):
    inst = create_visaobj(address)
    print_system_log(':MEAS?')
    res = inst.query(':MEAS?')
    result = e2float(res)
    print_system_log(result)
    return result


def send_commend_query(address, command):
    inst = create_visaobj(address)
    print_system_log('query--->'+command)
    result = inst.query(command)
    print_system_log('result--->')
    return result


def set_volt_and_current_style2(address, volt, current):
    print_system_log("set volt "+volt+"V，current "+current+"A")
    inst = create_visaobj(address)

    inst.write('VOLT '+volt)
    inst.write('CURR '+current)
    inst.write('OUTP ON')

    return 'ok'


def set_volt_and_current_for_charge(address, volt, current):
    print_system_log("set volt "+volt+"V，current "+current+"A")
    inst = create_visaobj(address)

    command = ":SOUR:VOLT "+volt
    inst.write(command)
    command = ":SOUR:CURR "+current
    inst.write(command)
    inst.write('OUTP1 ON')
    res = inst.query('READ?')
    print_system_log(res)
    res = eval(res)

    if type(res) ==tuple:
        data = res
    else:
        data = res.split(',')

    if float(data[0]) == float(volt) and float(data[1]) == float(current):
        print('ok')
        return 'ok'

def set_volt_and_current_for_battery(address, volt, current):
    print_system_log("set volt "+volt+"V，current "+current+"A")
    inst = create_visaobj(address)

    command = ":SOUR2:VOLT "+volt
    inst.write(command)
    command = ":SOUR2:CURR "+current
    inst.write(command)
    inst.write('OUTP2 ON')
    res = inst.query('READ2?')
    print_system_log(res)
    readv = e2float(res)
    if float(readv)-float(volt) <0.1:
        print('ok')
        return 'ok'

def set_volt_and_current(address, volt, current):
    print_system_log("set volt "+volt+"V，current "+current+"A")
    inst = create_visaobj(address)

    command = "APPL "+volt+","+current
    inst.write(command)
    inst.write('OUTP ON')
    res = inst.query('APPL?')
    print_system_log(res)
    res = eval(res)

    if type(res) ==tuple:
        data = res
    else:
        data = res.split(',')

    if float(data[0]) == float(volt) and float(data[1]) == float(current):
        print('ok')
        return 'ok'


def set_volt_and_current_for_3channel(sn, address,volt,cueernt):
    print_system_log('result--->')("set volt "+volt+"，current "+cueernt)
    inst = create_visaobj(address)
    inst.write('APPLy CH2, '+volt+', '+cueernt)
    print_system_log("OUTP ON")
    inst.write('OUTP 1')
    time.sleep(0.02)
    res = eval(send_commend_query(address, 'APPLy? CH2'))
    data = res.split(',')
    v = e2float(data[0])
    c = e2float(data[1])
    if float(v) == float(volt) and float(c) == float(cueernt):
        print_system_log("set ok")
        return 'ok'
    else:
        return 'Fail'


def get_volt_and_currebt_for_3channel(address):
    res = send_commend_query(address, 'APPLy? CH2')
    return res


def outpt_off_for_3channel(sn, address):
    send_commend_write(address, 'OUTP 0,(@2)')


def outpt_off_battery(address):
    send_commend_write(address, 'OUTP2 OFF')
    return 'ok'

def outpt_off(address):
    send_commend_write(address, 'OUTP OFF')
    return 'ok'


def send_commend_write(address, commend):
    #  'OUTP ON'
    #  'OUTP OFF'
    inst = create_visaobj(address)
    print_system_log('write-->'+commend)
    inst.write(commend)

def output_off_single(address,channel):
    send_commend_write(address, 'OUTPUT'+channel+' OFF')
    return 'ok'

def reset(address):
    inst = create_visaobj(address)
    print_system_log('reset')
    inst.write('*CLS')
    inst.write('*RST')


def create_sin(address,channel,frequence,volt):
    print_system_log('设置波形 SOURce'+channel+':Apply:Sin '+frequence+'Hz,'+volt)
    commend =  'SOURce'+channel+':Apply:Sin '+frequence+'Hz,'+volt
    # send_commend_write(address, 'SOURce1:Apply:Sin 10Hz,1')
    send_commend_write(address, commend)
    res = eval(send_commend_query(address, 'Source'+channel+':Apply?'))
    a = res.split()
    print_system_log(res)
    if 'SIN' in a[0]:
        print_system_log('设置成功')
        return 'ok'
        # params = a[1].split(',')
        # print(e2float(params[0]))
        # print(e2float(params[1]))
        # print(e2float(params[2]))

def create_squ(address,channel,frequence,volt,pwm):
    print_system_log('设置波形 SOURce'+channel+':Apply:SQU '+frequence+'Hz,'+volt)
    commend =  'SOURce'+channel+':APPL:SQU '+frequence+'Hz,'+volt
    # send_commend_write(address, 'SOURce1:Apply:Sin 10Hz,1')
    send_commend_write(address, commend)
    res = send_commend_query(address, 'Source'+channel+':Apply?')
    a = res.split()
    print_system_log(res)
    if 'SQU' in a[0]:
        print_system_log('设置SQU成功')
        print_system_log('设置占空比'+pwm)
        command = 'SOUR'+channel+':FUNC:SQU:DCYC '+pwm
        send_commend_write(address, command)
        send_commend_write(address, 'OUTPUT'+channel+' ON')

        return 'ok'
def sintest(address):
    # inst.write('SOURCE1:FUNCTION SIN')
    # inst.write('SOURCE1:FREQUENCY 1000')
    # inst.write('SOURCE1:VOLT:UNIT VPP')
    # inst.write('SOURCE1:VOLT 1')
    # inst.write('SOURCE1:VOLT:OFFSET 0')
    # inst.write('OUTPUT1:LOAD 50')
    # inst.write('OUTPUT1 ON')
    # inst.write('OUTPUT2 ON')
    # inst.write('SOURce2:Apply:Sin 10kHz,1.2')
    # # res = inst.query('Source1:Function?')
    # res = inst.query('Source2:Apply?')
    send_commend_write(address, 'SOURce1:Apply:Sin 10kHz,1')
    # res = inst.query('Source1:Function?')
    res = eval(send_commend_query(address, 'Source1:Apply?'))
    # inst.write('OUTPUT1 OFF')
    a = res.split()
    print(a)
    if 'SIN' in a[0]:

        params = a[0].split(',')
        print(e2float(params[1]))
        print(e2float(params[2]))
        print(e2float(params[3]))

        # if params[0]


def conf_volt_and_read(address):
    inst = create_visaobj(address)
    inst.write('CONF:VOLT:DC 100,0.01')
    time.sleep(0.02)
    res = e2float(inst.write('READ?'))
    return res

def get_volt_by_multimeter(address,range,precision):
    print_system_log("get volt")
    inst = create_visaobj(address)
    inst.write('CONF:VOLT:DC '+range+','+precision)
    time.sleep(1)
    res = inst.query('READ?')
    print_system_log(res)
    if ',' in res:
        data_list = res.split(',')
        data = e2float(data_list[0])
    elif '#9000000015' in res:
        res = res.replace('#9000000015','')
        data = e2float(res)
    else:
        data = e2float(res)
    print(data)
    return data


def get_current_by_multimeter(address,range,precision):
    print_system_log("get current")
    inst = create_visaobj(address)
    inst.write('CONF:CURR:DC '+range+','+precision)
    time.sleep(1)
    res = inst.query('READ?')
    print_system_log(res)
    if ',' in res:
        data_list = res.split(',')
        data = e2float(data_list[0])
    elif '#9000000015' in res:
        res = res.replace('#9000000015','')
        data = e2float(res)
    else:
        data = e2float(res)
    print(data)
    return data

def power_test_volt(address,channel):
    inst = create_visaobj(address)
    inst.write('CONF:VOLT:DC (@{})'.format(channel))
    inst.write('VOLT:DC:NPLC 20')
    res = inst.query('READ?')
    print_system_log(res)
    data_list = res.split(',')
    data = []
    for i in data_list:
        data.append(e2float(i))
    r ='|'.join(data)
    return r


def power_test_5v(address):
    print_system_log("Power Test 5V Start")
    inst = create_visaobj(address)
    inst.write('CONF:VOLT:DC (@111)')
    inst.write('VOLT:DC:NPLC 20')
    time.sleep(0.02)
    res = inst.query('READ?')
    print_system_log(res)
    data = e2float(res)
    return data


def close_channel(address,channel):
    print_system_log("close_channel{} Start".format(channel))
    inst = create_visaobj(address)
    inst.write('ROUT:OPEN (@201,202,203,204,205,206,207,208)')
    inst.write('ROUT:CLOS (@{})'.format(channel))
    res = inst.query('ROUT:CLOS? (@{})'.format(channel))
    data = res.rstrip('\n')
    if data == '1':
        print_system_log('close channel {} OK'.format(channel))
        return 'ok'

def open_channel(address,channel):
    print_system_log("open_channel{} Start".format(channel))
    inst = create_visaobj(address)
    inst.write('ROUT:OPEN (@{})'.format(channel))
    res = inst.query('ROUT:OPEN? (@{})'.format(channel))
    data = res.rstrip('\n')
    if data == '1':
        print_system_log('open channel {} OK'.format(channel))
        return 'ok'


def end_option(battery_address,dataswitch_address):
    print_system_log("open channel Start")
    inst = create_visaobj(dataswitch_address)
    inst.write('ROUT:OPEN (@204)')
    res = inst.query('ROUT:OPEN? (@204)')
    data = res.rstrip('\n')
    if data == '1':
        print_system_log('open channel 204 OK')
        outpt_off(battery_address)
        log.logger.info('battery OUTP OFF')
        return 'ok'


def measure_frequency(address):
    print_system_log("measure frequency")
    inst = create_visaobj(address)
    res = inst.query('MEAS:FREQ? (@1)')
    print_system_log(res)
    data = e2float(res)
    print(data)
    return data


def main():
    sn = '123'
    addr_counter = 'GPIB0::3::INSTR'  # 计数器
    addr_battery = 'GPIB0::8::INSTR'  # 电源
    addr_battery = 'USB0::0x2A8D::0x8F01::CN61390118::INSTR'  # 电源
    # addr_dataswitch = 'GPIB0::9::INSTR'  # 万用表
    addr_generator = 'GPIB0::10::INSTR'  # 波形发生器
    # 获取设备列表
    # get_manege_list()
    # # 获取设备详情
    # get_details(sn,addr_battery)
    # # reset(addr_battery)
    # get_current(addr_battery)
    # get_volt(addr_battery)
    # set_volt_and_current(sn,addr_battery,'5','0.5')
    # outpt_off(addr_battery)
    # get_current(addr_battery)
    # get_volt(addr_battery)
    # set_volt_and_current_for_3channel(sn,addr_battery,'5.2','1')
    # get_current(sn,addr_battery)
    # get_volt_and_currebt_for_3channel(addr_battery)
    # outpt_off_for_3channel(addr_battery)
    # sin(addr_generator)

    # power_test_3v3(sn, addr_dataswitch)
    # power_test_2v5(sn, addr_dataswitch)
    # measure_frequency(sn, addr_counter)
    # close_channel(sn,addr_dataswitch)
if __name__ == '__main__':
    main()
