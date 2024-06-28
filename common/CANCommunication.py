from PCANBasic import *
import threading
import time
import common.globalvar as gl

canbusInfo = {
    'CAN1': ['0x185', '0x1e0', '0x94', '0x54', '0x437'],
    'CAN2': ['0x55', '0x75', '0x95'],
    'CAN3': ['0x51', '0x71', '0x91'],
    'CAN4': ['0x50', '0x70', '0x90'],
    'GAC': ['0x7b9'],
    'GWM': ['000007C2']
}
channel_send_message = {
    "GAC": {
        "weak_up": [
            {"ID": 0X375, "DLC": 8, "data": "80 02 00 00 00 02 00 7E"},
        ],
        "video": [
            {"ID": 0X375, "DLC": 8, "data": "00 02 00 00 00 00 00 00"},
            {"ID": 0X2AB, "DLC": 8, "data": "00 00 00 00 00 00 00 00"},
        ]
    },
    "GWM": {
        "weak_up": [
            {"ID": 0X375, "DLC": 8, "data": "80 02 00 00 00 02 00 7E"},
        ],
        "video": [
            {"ID": 0X401, "DLC": 8, "data": "00 00 00 00 00 00 00 00"},
            {"ID": 0X119, "DLC": 8, "data": "00 05 02 00 00 00 00 00"},
        ]
    }

}


def SendCANMessage(objPCAN, channel, factory, type):
    weakupflag = gl.get_value('weakflag')
    while True:
        if type == 'weak_up':
            time.sleep(0.1)
        else:
            time.sleep(0.01)
        if weakupflag == 1:
            log.logger.info("weak up end")
            if channel == 1:
                if objPCAN.Uninitialize(PCAN_PCIBUS1) == PCAN_ERROR_OK:
                    log.logger.info("PCANBUS1 has release")
            elif channel == 2:
                if objPCAN.Uninitialize(PCAN_PCIBUS2) == PCAN_ERROR_OK:
                    log.logger.info("PCANBUS2 has release")
            elif channel == 3:
                if objPCAN.Uninitialize(PCAN_PCIBUS3) == PCAN_ERROR_OK:
                    log.logger.info("PCANBUS3 has release")
            elif channel == 4:
                if objPCAN.Uninitialize(PCAN_PCIBUS4) == PCAN_ERROR_OK:
                    log.logger.info("PCANBUS4 has release")
            break
        message_list = channel_send_message[factory][type]
        msg = TPCANMsg()
        msg.MSGTYPE = PCAN_MESSAGE_STANDARD
        for message in message_list:
            msg.ID = message['ID']
            msg.LEN = message['DLC']
            for index, value in enumerate(message['data'].split()):
                msg.DATA[index] = int(value, 16)
            #  The message is sent using the PCAN-USB Channel 1
            #
            if channel == 1:
                result = objPCAN.WriteFD(PCAN_PCIBUS1, msg)
            elif channel == 2:
                result = objPCAN.WriteFD(PCAN_PCIBUS2, msg)
            elif channel == 3:
                result = objPCAN.WriteFD(PCAN_PCIBUS3, msg)
            elif channel == 4:
                result = objPCAN.WriteFD(PCAN_PCIBUS4, msg)

            if result != PCAN_ERROR_OK:
                # An error occurred, get a text describing the error and show it
                #
                result = objPCAN.GetErrorText(result)
                print(result)
            else:
                print("Message sent successfully")


def CANWeakUp(sn,factory, channel, type='weak_up'):
    log = Logger(sn)
    gl._init()
    gl.set_value('log', log)
    gl.set_value('weakflag', 0)
    bitrate = "f_clock=24000000, nom_brp=3, nom_tseg1=13, nom_tseg2=2, nom_sjw=1, data_brp=2, data_tseg1=4, data_tseg2=1, data_sjw=1"
    if channel == '1':
        PCANBUS1 = PCANBasic()
        BUS1 = PCANBUS1.InitializeFD(PCAN_PCIBUS1, bytes(bitrate, 'utf-8'))
        if BUS1 == PCAN_ERROR_OK:
            tbus1write = threading.Thread(target=SendCANMessage, args=(PCANBUS1, 1, factory, type))
            tbus1write.start()
        else:
            res1 = PCANBUS1.GetErrorText(BUS1)
            log.logger.error(res1[1].decode('utf-8'))
        return PCANBUS1
    elif channel == '2':
        PCANBUS2 = PCANBasic()
        BUS2 = PCANBUS2.InitializeFD(PCAN_PCIBUS2, bytes(bitrate, 'utf-8'))
        if BUS2 == PCAN_ERROR_OK:
            tbus2write = threading.Thread(target=SendCANMessage, args=(PCANBUS2, 2, factory, type))
            tbus2write.start()
        else:
            res1 = PCANBUS2.GetErrorText(BUS2)
            log.logger.error(res1[1].decode('utf-8'))
        return PCANBUS2
    elif channel == '3':
        PCANBUS3 = PCANBasic()
        BUS3 = PCANBUS3.InitializeFD(PCAN_PCIBUS3, bytes(bitrate, 'utf-8'))
        if BUS3 == PCAN_ERROR_OK:
            tbus3write = threading.Thread(target=SendCANMessage, args=(PCANBUS3, 3, factory, type))
            tbus3write.start()
        else:
            res1 = PCANBUS3.GetErrorText(BUS3)
            log.logger.error(res1[1].decode('utf-8'))
        return PCANBUS3
    elif channel == '4':
        PCANBUS4 = PCANBasic()
        BUS4 = PCANBUS4.InitializeFD(PCAN_PCIBUS4, bytes(bitrate, 'utf-8'))
        if BUS4 == PCAN_ERROR_OK:
            tbus4write = threading.Thread(target=SendCANMessage, args=(PCANBUS4, 4, factory, type))
            tbus4write.start()
        else:
            res1 = PCANBUS4.GetErrorText(BUS4)
            log.logger.error(res1[1].decode('utf-8'))
        return PCANBUS4
    # if PCANBUS1.Uninitialize(PCAN_PCIBUS1) == PCAN_ERROR_OK:
    #     log.logger.info("PCANBUS1 已经被释放")

def get_message(data, type):
    res = get_filter_data(data)
    lenth = res['lenth']
    filter_data = res['data']
    if type != 'DTC':
        version = ''
        for i in range(lenth):
            version += chr(int(filter_data[i], 16))
        return version
    else:

        chunks = list(filter_data[i:i + 4] for i in range(0, lenth, 4))
        for i in chunks:
            log.logger.info(i)
        import difflib
        dd = difflib.get_close_matches(['5c', '40', '54'], chunks, cutoff=0.8)
        if dd:
            rr = int(dd[0][3], 16) & int('0x1', 16)
            if rr == 0:
                return 'ok'
            else:
                return 'fail'

        else:
            return 'ok'


def get_filter_data(data):
    split_start = 5
    filter_data = []
    for item in data:
        data_list = item[-1].split()
        if data_list[0] == '10':
            lenth = int(data_list[1], 16)
            filter_data += data_list[split_start:]
        else:
            if (8 - split_start) <= len(filter_data) and len(filter_data) <= lenth:
                filter_data += data_list[1:]
            else:
                break
    filter_data = filter_data[0:lenth]
    log.logger.info(filter_data)
    log.logger.info("lenth:" + str(lenth))
    return {'data': filter_data, 'lenth': lenth - 3}




def fota_gac_check(canbus, logFile, type, sn):
    log = Logger(sn)
    gl._init()
    gl.set_value('log', log)
    # python acu_ssh_script.py GAC|GWM|CAN1|CAN2 /Pcanlog/FOTA/GAC/1234/B/HW.log version
    import re
    testData = []
    logFile = os.path.join(os.path.dirname("D:\\CabbageTool\\Pcanlog")) + logFile
    rex = r"(.*?) - INFO: id:(" + "|".join(canbusInfo[canbus]) + ") data:(.*)"

    with open(logFile, 'r', encoding='UTF-8') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            # 正则匹配数据
            res = re.findall(rex, lines)
            if len(res) > 0:
                testData.append(res[0])
    result = get_message(testData, type)
    if type == 'HW':
        can_hw_version = config.get('GAC-A18-01', 'can_hw_version')
        if can_hw_version == result:
            log.logger.info('GAC_SW_V_APP_F1_81 Check PASS {} == {}'.format(result, can_hw_version))
            res = 'ok'
        else:
            log.logger.info('GAC_SW_V_APP_F1_81 Check FAIL {} != {}'.format(result, can_hw_version))
            res = 'fail'
    elif type == 'SW':
        can_sw_version = config.get('GAC-A18-01', 'can_sw_version')
        if can_sw_version == result:
            log.logger.info('GAC_SW_V_ECU_189 Check PASS {} == {}'.format(result, can_sw_version))
            res = 'ok'
        else:
            log.logger.info('GAC_SW_V_ECU_189 Check FAIL {} != {}'.format(result, can_sw_version))
            res = 'fail'
    else:
        if result == 'ok':
            log.logger.info('No Error Found in, DTC Error Test Passed')
            res = 'ok'
        else:
            log.logger.info('DTC Error')
            res = 'fail'
    return res