import os
import sys
from common.LogRecode import *
import time
from common.Configer import *
from common.UartCommunication import *
from common.helper import *
from BOARD_DC import *
from common.ModBus import *

isRunning = config(pathRunConfig, option='IsRunning')
gl._init()
if not isRunning:
    gl.set_value('DEBUG', True)
else:
    gl.set_value('DEBUG', False)


def test(params):
    create_log_debug(params)
    print_system_log('测试脚本示例', 2)
    return '2|4'


def CloseAllDevide(params):
    if params[0] == 'start':
        pass
    elif params[0] == 'end':
        pass
        # print('yyyyyyyyyy')
    elif params[0] == 'roundend':
        pass

        # print('zzzzzzzzzz')

if __name__ == '__main__':
    pass
    # channel_close(['USB0::0x2A8D::0x5101::MY58004896::INSTR','201'])
    # channel_open(['USB0::0x2A8D::0x5101::MY58004896::INSTR','201'])

    #print(power_on(['GPIB0::10::INSTR','7.4','2.0']))
    # print(uploadlogstoMES(('1')))
    # print(reset_device(['1']))
    # print(factory_rst_debug(['1']))
    # print(BLE_Signal_Quality_RX('1'))
    # exit()
    print(enable_CDC(['1']))
    print(enter_mfg_mode(['1']))
    print(factory_rst(['1']))
    # print(factory_rst_debug(['1']))
    print(enter_mfg_mode(['1']))
    exit()
    #print(test_emmc(['1']))
    print(get_imu_test(['1']))
    #print(festest(['1']))
    exit()
    # time.sleep(2)
    # print(measure_current(['GPIB0::10::INSTR']))
    # exit()
    # print(power_test_3v3(['USB0::0x2A8D::0x5101::MY58004896::INSTR']))
    # print(power_test_4v2(['USB0::0x2A8D::0x5101::MY58004896::INSTR']))
    print(measure_current_active(['GPIB0::10::INSTR']))

    print(enable_CDC(['1']))
    # set_iso_3v3_en([1])
    print(enter_mfg_mode(['1']))
    get_button_state(['1'])
    exit()
    # print(set_rdp(['1']))
    # time.sleep(1)
    # print(get_rdp(['1']))
    # print(sdram_test(['1']))
    # print(get_rdp(['1']))
    # print(set_MAX17205(['1']))
    # print(TEST_HV_FES(['0']))
    print(TEST_NEG_6V(['0']))
    # time.sleep(1)
    # print(SN_Provision(['0001000023400004']))
    # print(power_test_by_mult(['USB0::0x2A8D::0x5101::MY58004896::INSTR','101']))
    print(get_fw_version(['1']))
    # exit()
    # print(get_device_id(['1']))
    # print(get_ble_fw_version(['1']))
    # print(TEST_PMIC(['1']))
    # print(set_max_charging(['1']))
    # print(get_fuel_gage(['1']))
    # exit()
    print(set_mco_32k_en(['1']))
    # print(set_mco_32m_en(['1']))
    exit()
    # print(test_MCU_clock(['1']))
    # print(set_mco_32m_en(['1']))
    # meas_frequency(['USB0::0x0957::0x1807::MY62390325::INSTR'])
    # exit()
    # print(get_emmc_devid(['1']))
    # print(test_emmc(['1']))
    # print(read_temp(['1']))
    # print(fes_version(['1']))
    # print(test_FES_DAC_OUT(['3300']))
    # print(test_FES_DAC_OUT(['1650']))
    # print(test_FES_DAC_OUT(['0']))
    # print(festest(['0']))
    # print(get_imu_id(['1']))
    # print(get_imu_test(['1']))
    # print(get_button_state(['1']))
    # print(Enable_BLE_DTM_mode(['1']))
    # print(ext_dtm(['1']))
    # print(led_switch(['1','r','1']))
    # print(capture_color(['01']))
    # print(led_switch(['1','r','0']))
    # print(led_switch(['1','b','1']))
    # print(led_switch(['1','b','0']))
    # print(led_switch(['1','g','1']))
    # print(led_switch(['1','g','0']))
    #
    #
    # print(led_switch(['2','r','1']))
    # print(led_switch(['2','r','0']))
    # print(led_switch(['2','b','1']))
    # print(led_switch(['2','b','0']))
    # print(led_switch(['2','g','1']))
    # print(led_switch(['2','g','0']))
    # print(full_mux_test(['2']))
    # print(phy_devid(['2']))
    # print(phy_test(['2']))
    # time.sleep(1)
    # print(disable_3v3(['1']))
    # time.sleep(1)
    # print(enable_3v3(['1']))


    # print(set_mco_24m_en(['1']))
    # print(meas_frequency(['USB0::0x0957::0x1807::MY62170216::INSTR']))

    # JLink_program(['si2105_v190'])
    # power_test_4v2(['USB0::0x2A8D::0x5101::MY58004874::INSTR'])
    # power_on(['GPIB0::5::INSTR','4.2','0.1'])

    # print(create_single(['USB0::0x0957::0x2807::MY59003553::INSTR','1','500','0.02']))
    # channel_close(['USB0::0x2A8D::0x5101::MY58004874::INSTR','201'])
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','1']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','2']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','3']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','4']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','5']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','6']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','7']))
    # print(SNR_test(['USB0::0x2A8D::0x5101::MY58004874::INSTR','8']))

    # print(get_imu_id(['1']))
    # print(get_imu_test(['1']))

    # print(fx_up(['USB0::0x2A8D::0x5101::MY58004874::INSTR']))
    # print(fx_down(['USB0::0x2A8D::0x5101::MY58004874::INSTR']))
    # time.sleep(3)
    # print(rs485_send(['1']))
    print(rs485_receive(['1']))
    # print(set_rdp(['1']))
    # print(get_rdp(['1']))bn