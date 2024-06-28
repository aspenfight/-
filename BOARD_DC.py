import sys
import os
import time
import socket

from common.helper import *
from common.VisaCommunication import *
from common.UartCommunication import *
import threading
from common.MysqlHandle import *
from uploadtestfiles import *
# from check_path_exist_when_factory_rst import *


# def power_test_3v3(address):
#     inst = create_visaobj(address)
#     inst.write('CONF:VOLT:DC (@104,105)')
#     inst.write('VOLT:DC:NPLC 20')
#     time.sleep(0.02)
#     res = inst.query('READ?')
#     log.logger.info(res)
#     data_list = res.split(',')
#     data = e2float(data_list[0]) + '|' + e2float(data_list[1])
#     print(data)
#     return data

def check_station(params):
    create_log_debug(params)
    print_system_log("check station Start",2)
    table = 'recode_si'
    client = HandleMysql()
    sn = params[0]
    sql = "select * from " + table + " where sn='{}' and result='OK' order by id desc".format(sn)
    print_system_log(sql)
    res = client.query_sql(sql)
    print_system_log(res)
    if res is None:
        print_system_log('此产品与当前站位不匹配')
        return '站位不匹配'
    else:
        print_system_log('已测到到相关数据')
        return 'ok'

def uploadlogstoMES(params):
    create_log_debug(params)
    print_system_log("start uploadlogstoSERVER",2)
    connect_to_ftpserver('192.168.8.37', 21, 'testserver', 'test1234')
    UploadSummarylog('D:\CabbageTool\SummaryLog\DC-UNIT-debug', '\mpdata\SummaryLog')
    UploadLogAndSystemlog1('D:\CabbageTool\Log','\mpdata\Log')
    UploadLogAndSystemlog1('D:\CabbageTool\System log', '\mpdata\System log')
    print_system_log("uploadlogstoSERVER successfull",2)


def power_on(params):
    create_log_debug(params)
    address = params[0]
    volt = params[1]
    current = params[2]
    return set_volt_and_current_for_battery(address,volt,current)

def charge_on(params):
    create_log_debug(params)
    address = params[0]
    volt = params[1]
    current = params[2]
    set_volt_and_current_for_charge(address,volt,current)

def capture_color(params):
    create_log_debug(params)
    chn = params[0]
    print_system_log("Capture And Recoginse Start",2)
    try:
        res = send_commend_for_feasa('capture')
    except Exception as e:
        print_system_log(e)
        return e
    print_system_log(res.strip())
    if res.strip() == 'OK':
        response = send_commend_for_feasa('Getrgbi'+chn).strip()
        # response = '000 008 247 31950'
        print_system_log(response)
        color = response.split()
        r = color[0]
        g = color[1]
        b = color[2]
        # my_color = tuple(list(map(int, color[0:3])))
        # color = get_colorname(my_color)
        # log.logger.info(color)
        return r+'|'+g+'|'+b
    else:
        print_system_log('没有响应')

def send_commend_for_feasa(commend):
    print_system_log("send commend:"+commend)
    feasa_com = config(pathUartConfig, option='feasa')
    res = communiate(feasa_com, commend, 57600, "3", "0D0A")
    print_system_log(res)
    return res


def get_com_back():
    import serial.tools.list_ports

    all_comports = serial.tools.list_ports.comports()

    for comport in all_comports:
        if 'USB 串行设备' in comport.description:
            return comport.device
        # print(comport.device, comport.name, comport.description, comport.interface)


def factory_rst(params):
    create_log_debug(params)
    print_system_log('start factory rst', 2)
    res = send_commend_for_SI('factory_rst')
    print_system_log('factory_rst successful', 2)
    return 'ok'


def send_commend_for_SI(command, endsymbol="OK"):
    global Dongle_rs485_receive
    print_system_log("send commend:" + command)
    SIBoard_com = get_com()
    if 'full_mux_test' in command:
        timeout = "30"
    elif 'set_recovery' in command:
        timeout = "60"
    elif 'factory_rst' in command:
        timeout = "0"
    elif command == 'RST':
        timeout = "0"
    elif 'chg_set_lim' in command:
        timeout = "0"
    elif '0xfabfab02 1' in command:
        timeout = "0"
    else:
        timeout = "5"
    res = communiate(SIBoard_com, command, 115200, timeout, endsymbol, single=True)
    print_system_log(res)
    Dongle_rs485_receive = res
    if 'cmd=ERROR' in res:
        return 'fail'
    return res


def send_commend_for_Dongle(command, endsymbol="0D0A"):
    print_system_log("send commend:" + command)
    SIBoard_com = config(pathUartConfig, option='dongle')
    res = communiate(SIBoard_com, command, 3000000, "2", endsymbol, single=True)
    print_system_log(res)
    return res

def send_commend_for_golden_DC(command,endsymbol="OK"):
    print_system_log("send commend for goldenDC:" + command)
    goldenDC_com = config(pathUartConfig, option='goldenDC')
    res = communiate(goldenDC_com, command, 115200, "2", endsymbol, single=True)
    print_system_log(res)
    return res


def factory_rst(params):
    create_log_debug(params)
    print_system_log('start factory rst', 2)
    res = send_commend_for_SI('RST')
    print_system_log('factory_rst successful', 2)
    return 'ok'


def measure_current(params):
    create_log_debug(params)
    print_system_log('start measure current', 2)
    address = params[0]
    res = get_current_for_battery(address)
    print_system_log(res)
    return res


def measure_current_active(params):
    create_log_debug(params)
    print_system_log('start measure current', 2)
    address = params[0]
    res = []
    for i in range(5):
        c = get_current_for_battery(address)
        res.append(c)
    print_system_log(res)
    res_max= max(res)
    return res_max

def Power_Meter():
    import clr  # pythonnet
    clr.AddReference('mcl_pm_NET45')  # Reference the DLL
    from mcl_pm_NET45 import usb_pm
    pwr = usb_pm()  # Create an instance of the control class

    Status = pwr.Open_Sensor('')  # Connect the system (pass the serial number as an argument if required)

    if Status[0] > 0:  # The connection was successful

        ModelName = pwr.GetSensorModelName()
        SerialNo = pwr.GetSensorSN()
        print(ModelName, SerialNo)

        # Frequency measurement

        # pwr.FC_SetSampleTime = 500      # Set frequency sample
        Freq = pwr.FC_ReadFreq()  # Read frequency
        print_system_log(str(Freq) + "MHz")

        # Power measurement

        pwr.AvgCount = 2  # Set power measurement average count to 16
        pwr.AVG = 1  # Enable averaging
        Power = pwr.ReadPower()  # Read power
        print_system_log(str(Power) + "dBm")
        return str(Freq)+'|'+str(Power)

        # pwr.CloseSensor()               # Disconnect at the end of the program

    else:
        print("Could not connect.")

def meas_frequency(params):
    create_log_debug(params)
    print_system_log('start measure frequency', 2)
    address = params[0]
    res = measure_frequency(address)
    print_system_log(res)
    return res


def SNR_test(params):
    create_log_debug(params)
    address = params[0]
    channel = params[1]
    COM = params[2]
    print_system_log('start SNR_test 20{}'.format(channel), 2)
    close = channel_close([address, '20{}'.format(channel), params[-2], params[-1]])
    if close == 'ok':
        info = send_commend_for_SI('{} afe_signal_ch'.format(channel), 'OK')
        res = info.split()
        print(res)
        mean = res[-3].split('=')[-1].replace('uV,', '')
        std = res[-2].split('=')[-1].replace('uV', '')
        print(mean)
        print(std)
        time.sleep(0.1)
        send_commend_for_SI('ALL '+COM+' 1 ADSREG!', 'OK')
        time.sleep(0.1)
        send_commend_for_SI('ALL { 0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20 } ADSGAIN!', 'OK')
        time.sleep(0.1)
        send_commend_for_SI('1 ADSEN')
        time.sleep(0.1)
        res2 = send_commend_for_SI('EMGSNR!', 'aaa')
        fre_info = res2.split('==================================================')
        snr = fre_info[int(channel)].split(':')[-1].split()[0]
        return mean + '|' + std + '|' + snr


def create_single(params):
    create_log_debug(params)
    print_system_log('start create single', 2)
    address = params[0]
    channel = params[1]
    frequency = params[2]
    volt = params[3]
    res = create_sin(address, channel, frequency, volt)
    if res == 'ok':
        print_system_log('close channel ok')
        return 'ok'


def channel_close(params):
    create_log_debug(params)
    print_system_log('close channel', 2)
    address = params[0]
    channel = params[1]
    res = close_channel(address, channel)
    if res == 'ok':
        print_system_log('close channel ok')
        return 'ok'


def channel_open(params):
    create_log_debug(params)
    print_system_log('open channel', 2)
    address = params[0]
    channel = params[1]
    res = open_channel(address, channel)
    if res == 'ok':
        print_system_log('open channel ok')
        return 'ok'


def fx_up(params):
    create_log_debug(params)
    address = params[0]
    print_system_log('start create single', 2)
    inst = create_visaobj(address)
    inst.write('ROUT:OPEN (@219)')
    inst.write('ROUT:CLOS (@219)')
    res = inst.query('ROUT:CLOS? (@219)')
    print_system_log(res)
    data = res.rstrip('\n')
    if data == '1':
        print_system_log('close channel 219 OK')
        return 'OK'


def fx_down(params):
    create_log_debug(params)
    print_system_log('start create single', 2)
    address = params[0]
    inst = create_visaobj(address)
    inst.write('ROUT:OPEN (@220)')
    inst.write('ROUT:CLOS (@220)')
    res = inst.query('ROUT:CLOS? (@220)')
    print_system_log(res)
    data = res.rstrip('\n')
    if data == '1':
        print_system_log('close channel 220 OK')
        return 'OK'


# def power_on(params):
#     create_log_debug(params)
#     print_system_log('start power on', 2)
#     address = params[0]
#     volt = params[1]
#     current = params[2]
#     res = set_volt_and_current_style2(address, volt, current)
#     if res == 'ok':
#         print_system_log('power on successful')
#         return 'ok'
#     else:
#         return 'fail'


def charger_off(params):
    create_log_debug(params)
    address = params[0]
    res = outpt_off(address)
    if res == 'ok':
        print_system_log('power off successful')
        return 'ok'
    else:
        return 'fail'

def power_off(params):
    create_log_debug(params)
    address = params[0]
    res = outpt_off_battery(address)
    if res == 'ok':
        print_system_log('power off successful')
        return 'ok'
    else:
        return 'fail'


def power_test_4v2(params):
    create_log_debug(params)
    print_system_log('start test 4V2')
    address = params[0]
    res = power_test_volt(address, '103')
    print_system_log(res)
    return res

def power_test_by_mult(params):
    create_log_debug(params)
    address = params[0]
    channel = params[1]
    print_system_log('start test VOLT '+channel)

    res = power_test_volt(address, channel)
    print_system_log(res)
    return res



def power_test_3v3_EMG(params):
    create_log_debug(params)
    print_system_log('start test 3v3')
    address = params[0]
    res = power_test_volt(address, '101')
    print_system_log(res)
    return res


def power_test_3v3(params):
    create_log_debug(params)
    print_system_log('start test 3v3')
    address = params[0]
    res = power_test_volt(address, '102')
    print_system_log(res)
    return res

def power_test_4v2(params):
    create_log_debug(params)
    print_system_log('start test 4v2')
    address = params[0]
    res = power_test_volt(address, '101')
    print_system_log(res)
    return res


def JLink_program_back(params):
    create_log_debug(params)
    print_system_log('start JLink Flash', 2)
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)  # 成功返回True
    jlink.connect('STM32F411CE', 4000)  # 成功无返回
    print(jlink.core_id())
    print(jlink.device_family())
    print(jlink.target_connected())
    erase_status = jlink.erase()  # 成功返回0
    if erase_status == 0:
        print_system_log('erase success')
    file_path = 'D:\si_1221\{}.bin'.format(params[0])
    print_system_log('flash file->' + file_path)
    addr = 0x08000000
    res = jlink.flash_file(file_path, addr)  # 刷成功返回0，失败有多种原因
    jlink.reset()
    jlink.close()
    if res == 0:
        print_system_log('flash successful', 2)
        return 'ok'


def JLink_program(params):
    create_log_debug(params)
    # os.chdir("D:\si_1221")
    cmd = r"D:\si_1221\flash_si.bat"
    # res = os.system(cmd)
    # print('11111111')
    # os.system('exit')
    # print(res)
    # exit()
    # cmd = r"JLink.exe -device STM32F411CE -if SWD -speed 4000 -autoconnect 1 -CommandFile si.jlink"
    # subprocess 方式
    # import subprocess
    # sub = subprocess.Popen(cmd, shell=True, cwd="D:\\gen2program",stdout=subprocess.PIPE)
    # log.logger.info(sub.stdout.read())
    # result_list = subprocess.check_output(cmd, shell=True, cwd="D:\\gen2program",universal_newlines=True)
    # log.logger.info(result_list)
    # os.chdir("D:\\gen2program")
    # os.system("D:/gen2program/start.bat")

    # os.system方式
    # os.chdir("D:\\gen2program")
    # res = os.system("D:/gen2program/uuu -b emmc_all imx-boot fsp-image-core-fspimxv6-6.0.33.wic.bz2")
    # # res = os.system(cmd + "> /dev/null 2>&1")
    # log.logger.info(res)

    import subprocess
    p = subprocess.Popen(cmd, cwd="D:\\si_1221", stdout=subprocess.PIPE, shell=True)
    flag = 0
    for line in iter(p.stdout.readline, b''):
        linestr = line.decode('utf8').strip()
        print_system_log(linestr)
        if "Erasing down" in linestr:
            flag += 1
        if "O.K." in linestr:
            flag += 1

    p.communicate()
    p.stdout.close()
    if flag == 2:
        print_system_log('Program OK')
        return 'ok'
    else:
        return 'fail'


def enable_CDC(params):
    create_log_debug(params)
    print_system_log('start enable CDC', 2)
    res = send_commend_for_SI('0xfabfab02 1 " usb_usr" FORTH_USER_EN')
    # if 'cmd=OK' in res:
    print_system_log('enable CDC successful', 2)
    return 'ok'
    # else:
    #     return 'fail'

def TEST_HV_FES(params):
    create_log_debug(params)
    print_system_log('set HV_FES test in Volt', 2)
    res = send_commend_for_SI(params[0]+' fes_hv','OK')
    if 'cmd=OK' in res:
        print_system_log('set HV_FES test in Volt successful', 2)
        return 'ok'
    else:
        return 'fail'

def TEST_NEG_6V(params):
    create_log_debug(params)
    print_system_log('set NEG 6V test in Volt', 2)
    res = send_commend_for_SI(params[0]+' fes_neg','OK')
    if 'cmd=OK' in res:
        print_system_log('set NEG 6V test in Volt successful', 2)
        return 'ok'
    else:
        return 'fail'

def set_iso_3v3_en(params):
    create_log_debug(params)
    print_system_log('4.2V test in Volt', 2)
    res = send_commend_for_SI('1 iso_3v3_en','OK')
    if 'cmd=OK' in res:
        print_system_log('4.2V test in Volt successful', 2)
        return 'ok'
    else:
        return 'fail'


def set_MAX17205(params):
    create_log_debug(params)
    print_system_log('set MAX17205_SETNVM', 2)
    res = send_commend_for_SI('MAX17205_SETNVM', 'OK')
    if 'cmd=OK' in res:
        print_system_log('set MAX17205_SETNVM successful', 2)
        return 'ok'
    else:
        return 'fail'

def enter_mfg_mode(params):
    create_log_debug(params)
    print_system_log('start Enter mfg mode', 2)
    res = send_commend_for_SI('1 mfgmode','OK')
    if 'cmd=OK' in res:
        print_system_log('Enter mfg mode successful', 2)
        return 'ok'
    else:
        return 'fail'


def set_rdp(params):
    create_log_debug(params)
    print_system_log('start set rpd', 2)
    res = send_commend_for_SI('1 rdp','OK')
    time.sleep(2)
    if 'cmd=OK' in res:
        print_system_log('set rpd successful', 2)
        return 'ok'
    else:
        return 'fail'


def get_rdp(params):
    create_log_debug(params)
    print_system_log('start get rpd', 2)
    res = send_commend_for_SI('getrdp','OK')
    if 'cmd=OK' in res:
        rdp = res.split()[1].split('=')[-1]
        print_system_log('Get rpd successful', 2)
        return rdp
    else:
        return 'fail'


def SN_RESET(params):
    create_log_debug(params)
    sku = params[0][0:8]
    sn = params[0][8:16]
    print_system_log('start RESET sn', 2)
    res1 = send_commend_for_SI('ALL " 0xFABFAB02 reset_mfg_prov" siexec')
    if 'cmd=OK' in res1:
        time.sleep(0.5)
        print_system_log('reset sn successful', 2)
        time.sleep(1.0)
        send_commend_for_SI('RST')
        return 'ok'
    else:
        return 'fail'

def SN_Program(params):
    create_log_debug(params)
    sku = params[0][0:8]
    sn = params[0][8:16]

    print_system_log('start write sn', 2)
    # send_commend_for_SI('ALL " 0xFABFAB02 reset_mfg_prov" siexec')
    # time.sleep(1.0)
    res1 = send_commend_for_SI('ALL " 0x{} 0x{} set_serial" siexec'.format(sku, sn), 'OK')
    if 'cmd=OK' in res1:
        time.sleep(0.5)
        res4 = send_commend_for_SI('ALL " mfg_confirm" siexec', 'OK')
        if 'cmd=OK' in res4:
            print_system_log('write sn successful', 2)
            time.sleep(1.0)
            send_commend_for_SI('RST')
            return 'ok'
                # time.sleep(0.5)
                # res3 = send_commend_for_SI('GET_MFG', 'OK')
                # if 'cmd=OK' in res3:
                #     sn = res3.split()[2]
                #     print_system_log('write sn successful', 2)
                #     # send_commend_for_SI('RST')
                #     return sn
        else:
            return 'fail'



def SN_Provision(params):
    create_log_debug(params)
    sku = params[0][0:8]
    sn = params[0][8:16]

    print_system_log('start write sn', 2)
    send_commend_for_SI('0xFABFAB02 RESET_MFG_PROV', 'OK')
    time.sleep(0.5)
    res1 = send_commend_for_SI('0x{} 0x{} MFG_CONFIRM'.format(sku, sn), 'OK')
    if 'cmd=OK' in res1:
        time.sleep(0.5)
        res2 = send_commend_for_SI('SET_SERIAL', 'OK')
        if 'cmd=OK' in res2:
            time.sleep(0.5)
            res3 = send_commend_for_SI('GET_MFG', 'OK')
            if 'cmd=OK' in res3:
                print('333333333333333')
                sn = res3.split()[2]
                print_system_log('write sn successful', 2)
                # if
                return sn
            else:
                return 'fail'


def disable_3v3(params):
    create_log_debug(params)
    print_system_log('start disable 3v3', 2)
    res = send_commend_for_SI('emg_pwr_dis')
    if 'cmd=OK' in res:
        print_system_log('disable 3v3 successful', 2)
        return 'ok'
    else:
        return 'fail'


def enable_3v3(params):
    create_log_debug(params)
    print_system_log('start enable 3v3', 2)
    res = send_commend_for_SI('emg_pwr_en')
    if 'cmd=OK' in res:
        print_system_log('enable 3v3 successful', 2)
        return 'ok'
    else:
        return 'fail'


def get_fw_version(params):
    create_log_debug(params)
    print_system_log('start get fw_version', 2)
    res = send_commend_for_SI('fw_version')
    if 'cmd=OK' in res:
        version = eval(res.split()[1].split('=')[-1])
        print_system_log('get fw_version successful', 2)
        return version
    else:
        return 'fail'


def get_device_id(params):
    create_log_debug(params)
    print_system_log('start get device_id', 2)
    res = send_commend_for_SI('device_id','OK')
    if 'cmd=OK' in res:
        device_id = res.split()[1].split('=')[-1].strip("\"")
        print_system_log('get device_id successful', 2)
        return device_id
    else:
        return 'fail'


def get_fuel_gage(params):
    test_name = 'Verify FUEL Gage readings'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('fuel_gauge','OK')
    if 'cmd=OK' in res:
        device_id = res.split()[1].split('=')[-1].strip("\"")
        print_system_log('Set {} successful'.format(test_name), 2)
        return device_id
    else:
        return 'fail'

def set_max_charging(params):
    create_log_debug(params)
    print_system_log('start Set max charging value to 80%', 2)
    res = send_commend_for_SI('80 chg_set_lim','OK')
    if 'cmd=OK' in res:
        ress = res.split()[2].split('=')[-1].strip("\"")
        print_system_log('Set max charging value to 80% successful', 2)
        return ress
    else:
        return 'fail'

def set_delay_max_charging_75(params):
    create_log_debug(params)
    print_system_log('start Set delay max charging value to 75%', 1)
    send_commend_for_SI('40000 MS 75 chg_set_lim')
    print_system_log('Set delay max charging value to 75% successful', 1)
    return 'ok'


def TEST_PMIC(params):
    create_log_debug(params)
    print_system_log('start TEST pmic', 2)
    res = send_commend_for_SI('pmic_regs','OK')
    if 'cmd=OK' in res:
        # device_id = res.split()[1].split('=')[-1].strip("\"")
        print_system_log('get pmic successful', 2)
        return 'ok'
    else:
        return 'fail'

def get_ble_fw_version(params):
    create_log_debug(params)
    print_system_log('start get ble_fw_version', 2)
    res = send_commend_for_SI('ble_fw_version','OK')
    if 'cmd=OK' in res:
        device_id = res.split()[1].split('=')[-1].strip("\"")
        print_system_log('get ble_fw_version successful', 2)
        return device_id
    else:
        return 'fail'


def test_MCU_clock(params):
    test_name = 'Verify MCU clocks'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('clk', 'OK')
    if 'cmd=OK' in res:
        core_clk = res.split()[1].split('=')[-1].replace("MHz",'')
        print_system_log('{} successful'.format(test_name), 2)
        return core_clk
    else:
        return 'fail'


def set_mco_32k_en(params):
    test_name = 'mco_32k_en'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('mco_32k_en', 'OK')
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'


def get_emmc_devid(params):
    test_name = 'get_emmc_devid'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('emmc_devid', 'OK')
    if 'cmd=OK' in res:
        emmc_id = res.split()[1].split("=")[1].strip("\"")
        print_system_log('{} successful'.format(test_name), 2)
        return emmc_id
    else:
        return 'fail'

def festest(params):
    test_name = 'festest'
    create_log_debug(params)

    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('festest', 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'


def test_FES_DAC_OUT(params):
    scale = params[0]
    test_name = 'FES DAC_OUT scale '+scale
    create_log_debug(params)

    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('{} fes_dac_out'.format(scale), 'OK')
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'



def full_mux_test(params):
    test_name = 'full_mux_test'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('sudo_fes', 'OK')
    time.sleep(0.05)
    res = send_commend_for_SI('full_mux_test', 'OK')
    if res is None:
        res = send_commend_for_SI('full_mux_test', 'OK')
        if 'cmd=OK' in res:
            print_system_log('{} successful'.format(test_name), 2)
            return 'ok'
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'

def led_switch(params):
    create_log_debug(params)
    led_sn = params[0]
    type = params[1]
    status = params[2]
    test_name = 'LED{} {} {}'.format(led_sn,type,status)

    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('{} led{}_{}'.format(status,led_sn,type), 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'

def ext_dtm(params):
    test_name = 'Enable BLE DTM mode for external control'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('ext_dtm', 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'


def Enable_BLE_DTM_mode(params):
    test_name = 'Enable BLE DTM mode'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('dtm_prep', 'OK')
    time.sleep(0.1)
    res = send_commend_for_SI('50 255 7 dtm_tx', 'OK')
    # time.sleep(0.1)
    # res = send_commend_for_SI('3 dtm_rx', 'OK')
    time.sleep(15)
    fre = Power_Meter()
    res = send_commend_for_SI('dtm_stop', 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return fre
    else:
        return 'fail'

def Enable_BLE_DTM_mode_RX(params):
    test_name = 'Enable BLE DTM mode'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('dtm_prep', 'OK')
    time.sleep(0.1)
    res = send_commend_for_SI('3 dtm_rx', 'OK')
    time.sleep(15)
    fre = Power_Meter()
    res = send_commend_for_SI('dtm_stop', 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return fre
    else:
        return 'fail'

def BLE_Signal_Quality_RX(params):
    test_name = 'Enable BLE DTM mode RX'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    send_commend_for_golden_DC('0xfabfab02 1 " usb_usr" FORTH_USER_EN')
    send_commend_for_golden_DC('1 mfgmode','OK')
    res_goldenDC = send_commend_for_golden_DC('dtm_prep', 'OK')
    time.sleep(0.1)
    send_commend_for_SI('1 mfgmode', 'OK')
    res = send_commend_for_SI('dtm_prep', 'OK')
    time.sleep(0.1)
    res = send_commend_for_SI('30 dtm_rx', 'OK')
    time.sleep(0.1)
    # the golden unit is supposed to send 800 packets during the 2000ms test (1 packet / 2.5ms)
    res_goldenDC = send_commend_for_golden_DC('30 2000 dtm_ntx', 'OK')
    if 'cmd=OK' in res_goldenDC:
        res = send_commend_for_SI('dtm_stop', 'OK')
        # print(res)
        rcvd_packets = eval(res.split()[1].split('=')[-1])
        print_system_log(rcvd_packets)
        if 'cmd=OK' in res:
            print_system_log('{} successful'.format(test_name), 2)
            return rcvd_packets
        else:
            return 'fail'


def BLE_Signal_Quality_RX_golden_DC(params):
    test_name = 'Enable golden DC BLE DTM mode TX' #将golden DC设置成发送模式
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('dtm_prep', 'OK')
    time.sleep(0.1)
    res = send_commend_for_SI('30 2000 dtm_ntx', 'OK')
    if 'cmd=OK' in res:
        # print_system_log('{} successful'.format(test_name), 2)
        res = send_commend_for_SI('dtm_stop', 'OK')
        if 'cmd=OK' in res:
            print_system_log('{} successful'.format(test_name), 2)
            return 'ok'
        else:
            return 'fail'



def get_button_state(params):
    test_name = 'button state'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('button_state', 'OK')
    print(res)
    if 'cmd=OK' in res:
        state = res.split()[1].split("=")[1].strip("\"")
        print_system_log('{} successful'.format(test_name), 2)
        return state
    else:
        return 'fail'

def fes_version(params):
    test_name = 'fes_version'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('fes_version', 'OK')
    print(res)
    if 'cmd=OK' in res:
        emmc_id = res.split()[1].split("=")[1].strip("\"")
        print_system_log('{} successful'.format(test_name), 2)
        return emmc_id
    else:
        return 'fail'

def read_temp(params):
    test_name = 'temp_read'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('temp_read', 'OK')
    print(res)
    if 'cmd=OK' in res:
        emmc_id = res.split()[1].split("=")[1].strip("\"")
        print_system_log('{} successful'.format(test_name), 2)
        return emmc_id
    else:
        return 'fail'

def sdram_test(params):
    test_name = 'get_sdram_test'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('sdram_test', 'OK')
    print(res)
    if 'cmd=OK' in res:
        memset = res.split()[1].split("=")[1].replace("MB/s",'')
        memcpy = res.split()[2].split("=")[1].replace("MB/s",'')
        memcmp = res.split()[3].split("=")[1].replace("MB/s",'')

        print_system_log('{} successful'.format(test_name), 2)
        return memset+'|'+memcpy+'|'+memcmp
    else:
        return 'fail'

def phy_test(params):
    test_name = 'phy_test'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('phy_test', 'OK')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'

def phy_devid(params):
    test_name = 'phy_devid'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('phy_devid', 'OK')
    print(res)
    if 'cmd=OK' in res:
        phy_devid = res.split()[1].split("=")[1].strip("\"")

        print_system_log('{} successful'.format(test_name), 2)
        return phy_devid
    else:
        return 'fail'


def test_emmc(params):
    test_name = 'get_emmc_devid'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('emmc_test', 'OK')
    print(res)
    if 'cmd=OK' in res:
        emmc_rx = res.split()[1].split("=")[1].replace("KB/s",'')
        emmc_tx = res.split()[2].split("=")[1].replace("kB/s",'')

        print_system_log('{} successful'.format(test_name), 2)
        return emmc_rx+'|'+emmc_tx
    else:
        return 'fail'



def set_mco_32m_en(params):
    test_name = 'mco_32m_en'
    create_log_debug(params)
    print_system_log('start {}'.format(test_name), 2)
    res = send_commend_for_SI('mco_32m_en', '')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('{} successful'.format(test_name), 2)
        return 'ok'
    else:
        return 'fail'

def set_mco_24m_en(params):
    create_log_debug(params)
    print_system_log('start measure Frequency', 2)
    res = send_commend_for_SI('mco_24m_en', '')
    print(res)
    if 'cmd=OK' in res:
        print_system_log('measure Frequency successful', 2)
        return 'ok'
    else:
        return 'fail'


Dongle_receive = ''
Dongle_rs485_receive = ''


def read_uart(ser, timeout, endsymbol):
    while True:
        global Dongle_receive
        # if Dongle_receive != '':
        #     return
        ser.flush()
        _end = endsymbol
        if _end == '0D0A':
            _end = '\r\n'
        # reports = ''
        tickbegin = time.time()
        tickend = time.time()
        if (tickend - tickbegin) >= float(timeout):
            ser.flush()
            ser.close()
            return
        time.sleep(0.01)

        Dongle_receive += ser.read(ser.inWaiting()).decode('utf-8','ignore')
        print(Dongle_receive)
        # reports = reports.replace(ANSI_D, '')
        if endsymbol in Dongle_receive:
            ser.flush()
            ser.close()
            return

        if _end in Dongle_receive:
            ser.flush()
            ser.close()
            return
def get_SI_FW(params):
    create_log_debug(params)
    print_system_log('start get_SI_FW', 2)
    res = send_commend_for_SI('SI_FW')
    if 'cmd=OK' in res:
        version = eval(res.split()[1].split('=')[-1])
        print_system_log('get_SI_FW successful', 2)
        return version
    else:
        return 'fail'

def get_SIBNO_test(params):
    create_log_debug(params)
    print_system_log('start SIBNO', 2)
    res = send_commend_for_SI('SIBNO', endsymbol="OK")
    s1=s2=s3=s4=s5=s6 = ''
    if 'sec' in res:
        result = res.splitlines()
        print(result)
        for i in result:
            if 'mg' in i:
                s1 = i.split(',')[0].split('=')[1].replace('mg','')
                s2 = i.split(',')[1].replace('samples','').strip()
            if 'gyro' in i:
                a =  i.split('=')[1].split(',')
                s3 = a[0]
                s4 = a[1]
                s5 = a[2].replace('(mdeg/sec)','')
                s6 = a[3].replace('samples','').strip()
                # s3 =  i.split('=')[1].replace('(mdeg/sec)','').split('')
                # print(s3)

        # print(s1)
        # print(s2)
        # print(s3)
        # print(s4)
        # print(s5)
        # print(s6)
        # exit()

        # imu_id = eval(res.split()[-1].split('=')[-1])
        print_system_log('get SIBNO successful', 2)
        return s1 + '|' + s2 + '|' + s3 + '|' + s4 + '|' + s5 + '|' + s6
    else:
        return 'fail'

def rs485_send(params):
    global Dongle_receive
    create_log_debug(params)
    dongle_com = config(pathUartConfig, option='dongle')
    ser = serial.Serial(dongle_com, 3000000, timeout=float(5), xonxoff=True)
    dongle_uart = threading.Thread(target=read_uart, args=(ser, 5, 'rs485'))
    dongle_uart.start()
    print_system_log('start test rs485 send', 2)
    for i in range(3):
        time.sleep(0.5)
        res = send_commend_for_SI('3000000 rs485_send', endsymbol="OK")
        print(res.splitlines())
        if 'cmd=OK' in res:
            info = eval(res.splitlines()[2].split('=')[-1])
            print_system_log(info)
            time.sleep(1)
            # donngle_receive = send_commend_for_Dongle('')
            print_system_log('dongle receive')
            print_system_log(Dongle_receive)
            if info == Dongle_receive:
                print_system_log('send rs485 successful', 2)
                return 'ok'
        else:
            return 'fail'


def rs485_receive(params):
    global Dongle_rs485_receive
    create_log_debug(params)
    print_system_log('start test rs485 receive', 2)
    dongle_uart = threading.Thread(target=send_commend_for_SI_485, args=('3000000 rs485_receive', 'OK'))
    dongle_uart.start()
    time.sleep(2)
    send_commend_for_Dongle('test rs485')
    time.sleep(5)
    print(Dongle_rs485_receive)

    if 'test rs485' in Dongle_rs485_receive:
        print_system_log('rs485_receive successful', 2)
        return 'ok'
    else:
        return 'fail'


def Set_Recovery(params):
    import shutil
    create_log_debug(params)
    # os.popen("copy D:\\v1.10.9\\apollo_img.cionic F:\\apollo_img.cionic")
    p = shutil.copy("D:\\v1.10.9\\apollo_img.cionic","E:\\apollo_img.cionic")
    print_system_log("copy files to " + p + " successful")
    res3 = send_commend_for_SI('" sd0:/apollo_img.cionic" set_recovery', 'OK')
    if 'cmd=OK' in res3:
        print_system_log('set recovery successful', 2)
        return 'ok'
    else:
        return 'fail'


def Disable_CDC(params):
    create_log_debug(params)
    res3 = send_commend_for_SI('0xfabfab02 0 " usb_usr" FORTH_USER_EN', 'OK')
    if 'cmd=OK' in res3:

        print_system_log('Disable CDC successful', 2)
        return 'ok'
    else:
        return 'fail'


def get_imu_id(params):
    create_log_debug(params)
    print_system_log('start get imu_id', 2)
    res = send_commend_for_SI('imu_id', endsymbol="OK")
    print(res)
    if 'cmd=OK' in res:
        imu_id = res.split()[1].split('=')[-1].strip("\"")
        print_system_log('get imu_id successful', 2)
        return imu_id
    else:
        return 'fail'


def get_imu_test(params):
    create_log_debug(params)
    print_system_log('start imu_test', 2)
    res = send_commend_for_SI('imu_test', endsymbol="OK")
    if 'sec' in res:
        result = res.split()
        print(result)
        s1 = result[1].split('=')[1].replace('mg','')
        s2 = result[3]
        s3, s4, s5 = result[5].split('=')[1].replace('(mdeg/sec)','').split(',')
        s6 = result[7]
        # imu_id = eval(res.split()[-1].split('=')[-1])
        print_system_log('get imu_test successful', 2)
        return s1 + '|' + s2 + '|' + s3 + '|' + s4 + '|' + s5 + '|' + s6
    else:
        return 'fail'

def get_com(timeout=30):
    import serial.tools.list_ports
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError("Timed out while searching for a USB serial device.")
        all_comports = serial.tools.list_ports.comports()
        for comport in all_comports:
            if 'USB 串行设备' in comport.description:
                return comport.device
        time.sleep(1)

def send_commend_for_reset_device(command, endsymbol="OK"):
    # print_system_log("send commend:" + command)
    SIBoard_com = get_com()
    print(SIBoard_com)
    if 'full_mux_test' in command:
        timeout = "30"
    elif 'set_recovery' in command:
        timeout = "60"
    elif 'factory_rst' in command:
        timeout = "0"
    elif 'chg_set_lim' in command:
        timeout = "0"
    elif '0xfabfab02 1' in command:
        timeout = "0"
    else:
        timeout = "5"
    res = communiate(SIBoard_com, command, 115200, timeout, endsymbol, single=True)
    # print_system_log(res)
    if 'cmd=ERROR' in res:
        return 'fail'
    return res

def reset_device(params):
    print_system_log("start factory rst...")
    print("start factory rst...")
    res1 = send_commend_for_reset_device('0xfabfab02 1 " usb_usr" FORTH_USER_EN')
    res2 = send_commend_for_reset_device('1 mfgmode','OK')
    res3 = send_commend_for_reset_device('factory_rst')

def check_and_reset_device_until_path_exists(params):
    retries = 0
    while retries < 5:#retries次数小于m
        reset_device(params)  # 重置设备
        time.sleep(12)  # 等待n秒
        if os.path.exists("E:\\"):
            print_system_log('emmc path exist')
            return "ok"  # 路径存在，返回OK
        retries += 1
    # 如果超过最大重试次数，则返回错误信息
    return "Error: Emmc Path does not exist after multiple retries."

def factory_rst_debug(params):
    create_log_debug(params)
    print_system_log('start factory rst',2)
    result = check_and_reset_device_until_path_exists(params)
    if 'ok' in result:
        print_system_log("factory rst successful",2)
        return result
    else:
        print_system_log(result)
        return result

