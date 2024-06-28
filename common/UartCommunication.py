import serial
import time

import serial
import time


def connect_serial(port_name, baud_rate, timeout):
    try:
        ser = serial.Serial(port_name, baud_rate, timeout=float(timeout),xonxoff=True)
        return ser
    except serial.SerialException as e:
        print(f"串口通信错误: {e}")
        return None


def communiate(port_name, commend, baud_rate, timeout, endsymbol, enter=True,single=False, max_retries=3):
    if commend.startswith('MUX:'):
        rt = communiate_mux(port_name, commend, baud_rate, timeout, endsymbol)
        return rt
    if enter:
        if commend !='RST':
            commend += '\r\n'
        else:
            commend += '\r'
    for attempt in range(max_retries):
        ser = connect_serial(port_name, baud_rate, timeout)
        if ser is not None:
            try:
                ser.flush()
                if single:
                    for i in commend:
                        ser.write(i.encode())
                        time.sleep(0.001)
                else:
                    data = commend.encode()
                    ser.write(data)

                # timeout==0 表示只写不读
                if float(timeout) == 0:
                    ser.flush()
                    ser.close()
                    return ''

                _end = endsymbol
                if _end == '0D0A':
                    _end = '\r\n'
                reports = ''
                tickbegin = time.time()
                while True:
                    tickend = time.time()
                    if (tickend - tickbegin) >= float(timeout):
                        ser.flush()
                        ser.close()
                        break
                    time.sleep(0.01)

                    reports += ser.read(ser.inWaiting()).decode()
                    if not endsymbol == 'no endSymble':
                        # reports = reports.replace(ANSI_D, '')
                        if endsymbol in reports:
                            ser.flush()
                            ser.close()
                            return reports

                        if _end in reports:
                            ser.flush()
                            ser.close()
                            return reports
                            # break

                return reports
            except serial.SerialException as e:
                print(f"在通信过程中发生串口错误: {e}")
                ser.close()  # 清理并关闭串口
            except Exception as e:
                print(f"在通信过程中发生其他错误: {e}")
                ser.close()  # 清理并关闭串口
        else:
            print(f"尝试 {attempt + 1} 失败，等待后重试...")
            time.sleep(5)  # 等待一段时间后重试

    # 如果所有尝试都失败了，返回None或其他错误指示符
    return "please retest"


def communiate_back(port_name, commend, baud_rate, timeout, endsymbol, enter=True,single=False):
    if commend.startswith('MUX:'):
        rt = communiate_mux(port_name, commend, baud_rate, timeout, endsymbol)
        return rt
    if enter:
        if commend !='RST':
            commend += '\r\n'
        else:
            commend += '\r'
    ser = serial.Serial(port_name, baud_rate, timeout=float(timeout),xonxoff=True)
    # ser.read(ser.inWaiting())
    ser.flush()
    if single:
        for i in commend:
            ser.write(i.encode())
            time.sleep(0.001)
    else:
        data = commend.encode()
        ser.write(data)

    # timeout==0 表示只写不读
    if float(timeout) == 0:
        ser.flush()
        ser.close()
        return ''

    _end = endsymbol
    if _end == '0D0A':
        _end = '\r\n'
    reports = ''
    tickbegin = time.time()
    while True:
        tickend = time.time()
        if (tickend - tickbegin) >= float(timeout):
            ser.flush()
            ser.close()
            break
        time.sleep(0.01)

        reports += ser.read(ser.inWaiting()).decode()
        if not endsymbol == 'no endSymble':
            # reports = reports.replace(ANSI_D, '')
            if endsymbol in reports:
                ser.flush()
                ser.close()
                return reports

            if _end in reports:
                ser.flush()
                ser.close()
                return reports
                # break

    return reports




def communiate_mux(port_name, commend, baud_rate, timeout, endsymbol):
    reports = ''
    commend = commend.replace("MUX:", "")
    ser = serial.Serial(port_name, baud_rate, timeout=float(timeout))
    ser.flush()
    # first close all
    ser.write(b"\xAA\x00\x00\x00\x00\x00\xBB")
    n = ser.inWaiting()
    sss = ser.read()

    if sss == b'\x00':
        print("CloseAllOK")
    else:
        ser.flush()
        ser.close()
        print('mux close all time out')
        return 'mux close all time out'

    if int(commend) == 0:
        ser.write(b"\xAA\x00\x00\x00\x00\x00\xBB")
    elif int(commend) == 1:
        ser.write(b"\xAA\x01\x00\x00\x00\x00\xBB")
    elif int(commend) == 2:
        ser.write(b"\xAA\x01\x01\x00\x00\x00\xBB")
    elif int(commend) == 3:
        ser.write(b"\xAA\x01\x02\x00\x00\x00\xBB")
    elif int(commend) == 4:
        ser.write(b"\xAA\x01\x03\x00\x00\x00\xBB")
    elif int(commend) == 5:
        ser.write(b"\xAA\x01\x04\x00\x00\x00\xBB")
    elif int(commend) == 6:
        ser.write(b"\xAA\x01\x05\x00\x00\x00\xBB")
    elif int(commend) == 7:
        ser.write(b"\xAA\x01\x06\x00\x00\x00\xBB")
    elif int(commend) == 8:
        ser.write(b"\xAA\x01\x07\x00\x00\x00\xBB")
    elif int(commend) == 9:
        ser.write(b"\xAA\x01\x08\x00\x00\x00\xBB")
    elif int(commend) == 10:
        ser.write(b"\xAA\x01\x09\x00\x00\x00\xBB")
    elif int(commend) == 11:
        ser.write(b"\xAA\x01\x0B\x00\x00\x00\xBB")
    elif int(commend) == 12:
        ser.write(b"\xAA\x01\x0c\x00\x00\x00\xBB")
    elif int(commend) == 13:
        ser.write(b"\xAA\x01\x0d\x00\x00\x00\xBB")
    elif int(commend) == 14:
        ser.write(b"\xAA\x01\x0e\x00\x00\x00\xBB")
    elif int(commend) == 15:
        ser.write(b"\xAA\x01\x0f\x00\x00\x00\xBB")
    elif int(commend) == 16:
        ser.write(b"\xAA\x01\x10\x00\x00\x00\xBB")
    elif int(commend) == 17:
        ser.write(b"\xAA\x01\x11\x00\x00\x00\xBB")
    elif int(commend) == 18:
        ser.write(b"\xAA\x01\x12\x00\x00\x00\xBB")
    elif int(commend) == 19:
        ser.write(b"\xAA\x01\x13\x00\x00\x00\xBB")
    elif int(commend) == 20:
        ser.write(b"\xAA\x01\x14\x00\x00\x00\xBB")
    elif int(commend) == 21:
        ser.write(b"\xAA\x01\x15\x00\x00\x00\xBB")
    elif int(commend) == 22:
        ser.write(b"\xAA\x01\x16\x00\x00\x00\xBB")
    elif int(commend) == 23:
        ser.write(b"\xAA\x01\x17\x00\x00\x00\xBB")
    elif int(commend) == 24:
        ser.write(b"\xAA\x01\x18\x00\x00\x00\xBB")

    n = ser.inWaiting()
    sss = ser.read()

    if sss == b'\x01':
        print("Mux Open bit OK")
    else:
        ser.flush()
        ser.close()
        print('mux open bit time out')
        return 'mux open bit time out'

    ser.flush()
    ser.close()

    return reports


def communiate_modbus(port_name, commend, baud_rate, timeout, endsymbol):
    reports = b''
    ser = serial.Serial(port_name, baud_rate, timeout=float(timeout))
    ser.flush()
    # first close all
    # ser.write(b"\xAA\x00\x00\x00\x00\x00\xBB")
    # n = ser.inWaiting()
    # sss = ser.read()
    #
    # if sss == b'\x00':
    #     print("CloseAllOK")
    # else:
    #     ser.flush()
    #     ser.close()
    #     print('mux close all time out')
    #     return 'mux close all time out'

    ser.write(commend)
    _end = endsymbol
    if _end == '0D0A':
        _end = '\r\n'
    tickbegin = time.time()
    while True:
        tickend = time.time()
        if (tickend - tickbegin) >= float(timeout):
            ser.flush()
            ser.close()
            break
        time.sleep(0.001)

        reports += ser.read(ser.inWaiting())

        if not endsymbol == 'no endSymble':
            # reports = reports.replace(ANSI_D, '')
            if endsymbol in reports:
                ser.flush()
                ser.close()
                return reports

            if _end in reports:
                ser.flush()
                ser.close()
                return reports
                # break
    return reports

def String2Hex(string):
    res = bytes(bytearray.fromhex(string))
    return res
