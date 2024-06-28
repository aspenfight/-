import os
import time
import ftplib
from ftplib import error_perm
from common.LogRecode import *
import os
from datetime import datetime,timedelta
import glob
#创建一个ftp对象
ftp = ftplib.FTP()
# 连接FTP服务器
def connect_to_ftpserver(ftp_server_ip,ftp_port,ftp_username,ftp_password):
    ftp.connect(ftp_server_ip, ftp_port)
    ftp.login(ftp_username, ftp_password)
    print("connect")

# 遍历本地文件夹并上传文件
def upload_files(local_folder_path,ftp_folder_path):
    for foldername in os.listdir(local_folder_path):
        current_local_path = os.path.join(local_folder_path, foldername)
        # print(current_local_path)
        current_ftp_path = os.path.join(ftp_folder_path, foldername)
        # print(current_ftp_path)
    # 创建目标FTP文件夹（如果不存在）
    #     print(os.getcwd())
        ftp.cwd(ftp_folder_path)
        folders_list = ftp.nlst()
        print("打印远程文件夹列表")
        print(folders_list)
        if foldername in ftp.nlst():
            for file in os.listdir(current_local_path):
                # print(os.getcwd())
                # print(f"处理该文件:{file}")
                print("服务器文件夹在本地文件夹列表中")
                local_file_path = os.path.join(current_local_path, file)
                # print(current_local_path)
                target_file_path = os.path.join(current_ftp_path,file)
                # print(target_file_path)
                ftp.cwd(current_ftp_path)
                file_list = ftp.nlst()
                print(file_list)
                if file not in file_list:
                    print(f"处理该文件:{file}")
                    with open(local_file_path, 'rb') as f:
                        ftp.storbinary('STOR ' + target_file_path, f)
                        print("传输成功")
                        # 上传文件到FTP服务器
        elif foldername == "Buffer":
            pass
        elif foldername == "SYS":
            pass
        elif foldername not in ftp.nlst():
            ftp.mkd(foldername)
            # 否则，需要遍历当前文件夹文件，远程服务器没有的文件，需要传至远程服务器文件夹
            for file in os.listdir(current_local_path):
                # print(os.getcwd())
                # print(f"处理该文件:{file}")
                local_file_path = os.path.join(current_local_path, file)
                print(current_local_path)
                target_file_path = os.path.join(current_ftp_path,file)
                print(target_file_path)
                with open(local_file_path, 'rb') as f:
                    ftp.storbinary('STOR ' + target_file_path, f)
                    print("传输完成")
#    time.sleep(10)
#遍历指定路径文件夹内文件，将其传至ftp服务器指定路径下
def upload_summarylog_files(local_folder_path,ftp_folder_path):
    for foldername in os.listdir(local_folder_path):
        current_local_path = os.path.join(local_folder_path, foldername)
        # print(current_local_path)
        current_ftp_path = os.path.join(ftp_folder_path, foldername)
        # print(current_ftp_path)
    # 创建目标FTP文件夹（如果不存在）
    #     print(os.getcwd())
    #     print_system_log(current_local_path)
        ftp.cwd(ftp_folder_path)
        folders_list = ftp.nlst()
        print("打印服务器文件夹列表")
        print(folders_list)
        if foldername in ftp.nlst():
            for file in os.listdir(current_local_path):
                # print(os.getcwd())
                # print(f"处理该文件:{file}")
                print("服务器文件夹在本地文件夹列表中")
                local_file_path = os.path.join(current_local_path, file)
                # print(current_local_path)
                target_file_path = os.path.join(current_ftp_path,file)
                # print(target_file_path)
                with open(local_file_path, 'rb') as f:
                    ftp.storbinary('STOR ' + target_file_path, f)
                    print("传输成功")
                    print_system_log("summarylog传输成功")
                    # 上传文件到FTP服务器
        elif foldername == "Buffer":
            pass
        elif foldername == "SYS":
            pass
        elif foldername not in ftp.nlst():
            ftp.mkd(foldername)
            # 否则，需要遍历当前文件夹文件，远程服务器没有的文件，需要传至远程服务器文件夹
            for file in os.listdir(current_local_path):
                # print(os.getcwd())
                # print(f"处理该文件:{file}")
                local_file_path = os.path.join(current_local_path, file)
                print(current_local_path)
                target_file_path = os.path.join(current_ftp_path,file)
                print(target_file_path)
                with open(local_file_path, 'rb') as f:
                    ftp.storbinary('STOR ' + target_file_path, f)
                    print("传输完成")
                    # print_system_log("summarylog传输成功")

def is_recent_1_days(path):
    """
    检查文件夹是否在最近几天内被修改过
    """
    # 获取文件夹的最后修改时间（时间戳）
    mtime = os.path.getmtime(path)

    # 获取当前时间的时间戳
    now = time.time()

    # 计算最近几天的时间戳（假设1天为例）
    one_month_ago = now - (1 * 24 * 60 * 60)

    # 如果文件夹的最后修改时间大于1天前的时间戳，则认为它是最近1天前的
    return mtime > one_month_ago

def check_ftp_folder_exists(ftp, folder_path):
    """
    检查FTP服务器上指定的文件夹是否存在。
    如果存在，返回True；否则返回False。
    """
    try:
        ftp.cwd(folder_path)
        return True
    except error_perm:
        return False

#定义一个函数，遍历当天文件夹内的文件，作出判断，并且传输到服务器上
def UploadLogAndSystemlog(local_folder_path,ftp_folder_path):
    # 获取当前日期并格式化为字符串
    today = datetime.now().strftime('%Y-%m-%d')
    current_local_path = os.path.join(local_folder_path,today)
    current_ftp_path = os.path.join(ftp_folder_path,today)
    check = check_ftp_folder_exists(ftp,current_ftp_path)
    if not check:
        ftp.mkd(current_ftp_path)
    for file in os.listdir(current_local_path):
    # print(os.getcwd())
    # print(f"处理该文件:{file}")
        local_file_path = os.path.join(current_local_path, file)
        print(local_file_path)
        target_file_path = os.path.join(current_ftp_path,file)
        print(target_file_path)
        ftp.cwd(current_ftp_path)
        files_list = ftp.nlst()
        if file not in files_list:
            with open(local_file_path, 'rb') as f:
                ftp.storbinary('STOR ' + target_file_path, f)
                print_system_log("upload log to SERVER")
                print("传输完成")

#定义一个函数，处理指定文件夹内最近生成的1个文件，将文件传输到服务器上
def UploadLogAndSystemlog1(local_folder_path,ftp_folder_path):
    # 获取当前日期并格式化为字符串
    today = datetime.now().strftime('%Y-%m-%d')
    current_local_path = os.path.join(local_folder_path,today)
    current_ftp_path = os.path.join(ftp_folder_path,today)
    check = check_ftp_folder_exists(ftp,current_ftp_path)
    if not check:
        ftp.mkd(current_ftp_path)
    latest_files = get_latest_files(current_local_path,1)
    for local_file_path in latest_files:
        print(local_file_path)
        file = os.path.basename(local_file_path)
        target_file_path = os.path.join(current_ftp_path,file)
        print(target_file_path)
        with open(local_file_path, 'rb') as f:
            ftp.storbinary('STOR ' + target_file_path, f)
            # print_system_log("upload log to SERVER")
            print("传输完成")

# 定义一个函数，处理指定文件夹内最近生成的1个文件，将文件传输到服务器上
def UploadSummarylog(local_folder_path,ftp_folder_path):
    today = datetime.now().strftime('%Y%m%d')
    # print_system_log(today)
    current_local_path = os.path.join(local_folder_path,today)
    current_ftp_path = os.path.join(ftp_folder_path,today)
    print(current_ftp_path)
    check = check_ftp_folder_exists(ftp,current_ftp_path)
    if not check:
        ftp.mkd(current_ftp_path)
    latest_files = get_latest_files(current_local_path,1)
    for local_file_path in latest_files:
        print(local_file_path)
        file = os.path.basename(local_file_path)
        target_file_path = os.path.join(current_ftp_path,file)
        print(target_file_path)
        with open(local_file_path, 'rb') as f:
            ftp.storbinary('STOR ' + target_file_path, f)
            print_system_log("upload summarylog to SERVER")
            print("传输完成")

#定义一个函数，在指定文件夹路径里，找到最近生成的num_files个文件，参数directoty为绝对路径
def get_latest_files(directory, num_files):
    # 获取文件夹内所有文件的完整路径
    file_paths = glob.glob(os.path.join(directory, '*'))

    # 过滤出文件，排除文件夹
    files = [path for path in file_paths if os.path.isfile(path)]

    # 按照文件的修改时间进行排序
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # 返回最近的num_files个文件
    return files[:num_files]


def main():
    pass
    connect_to_ftpserver('192.168.8.37',21,'testserver','test1234')
    # upload_files(log_path,log_ftp_path)
    # upload_summarylog_files('D:\CabbageTool\SummaryLog\DC-UNIT-debug', '\mpdata\SummaryLog')
    UploadSummarylog('D:\CabbageTool\SummaryLog\DC-UNIT-debug', '\mpdata\SummaryLog')
    # upload_files(systemlog_path, systemlog_ftp_path)
    # UploadLogAndSystemlog1('D:\CabbageTool\Log', '\mpdata\Log')
    # UploadLogAndSystemlog('D:\CabbageTool\Log', '\mpdata\Log')

if __name__ == "__main__":
    pass
    # while True:
    main()
        # time.sleep(regular_upload_time1)
