import os
import time
from common.LogRecode import *
from BOARD_DC import *

def reset_device():
    # 这里假设这个函数是用来重置设备的
    # 在实际中，你需要用实际的重置逻辑来替换这个print语句
    print("Resetting the device...")
    # time.sleep(0.5)
    # 你可以在这里调用你的设备重置API或命令
    # ...

def check_path_exists(path):
    # 检查路径是否存在
    return os.path.exists(path)

def check_and_reset_device_until_path_exists(device_path, max_retries=2):  # 假设我们尝试5次
    retries = 0
    while retries < max_retries:
        reset_device()  # 重置设备
        time.sleep(3)  # 等待10秒
        if check_path_exists(device_path):
            return "ok"  # 路径存在，返回OK
        retries += 1
    # 如果超过最大重试次数，则返回错误信息
    return "Error: Path does not exist after multiple retries."

# 使用示例
def main():
    device_path = "F:\\"  # 替换为你的设备路径
    result = check_and_reset_device_until_path_exists(device_path)
    print(result)

if __name__ == '__main__':
    main()