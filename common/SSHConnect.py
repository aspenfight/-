import common.globalvar as gl
import pexpect.popen_spawn
from common.LogRecode import *
from common.Configer import *


def login_product(host, username, timeout=30, password='ubuntu'):
    timeout = timeout
    log = gl.get_value('log')
    cmd = 'plink.exe -ssh -v {}@{} -P 22 -pw {}'.format(username, host, password)
    # cmd = 'plink.exe -ssh -v ubuntu@192.168.1.12 -P 22 -pw ubuntu'
    log.logger.info('ssh execute command:{}'.format(cmd))
    ssh_handle = pexpect.popen_spawn.PopenSpawn(cmd, timeout=timeout)
    exp = ssh_handle.expect(['y/n', 'session'])

    if exp == 0:
        exp1 = execute_cmd_by_ssh(ssh_handle, 'y', prompt=[username + '@'])
        if exp1 == 0:
            log.logger.info('login success')
            return ssh_handle
    elif exp == 1:
        exp2 = execute_cmd_by_ssh(ssh_handle, '', prompt=[username + '@'])
        if exp2 == 0:
            log.logger.info('login success')
            return ssh_handle


def login_ubuntu(host, timeout=30):
    log = gl.get_value('log')
    timeout = timeout
    cmd = 'plink.exe -ssh -v k@{} -P 22 -pw 1234560'.format(host)
    # cmd = 'plink.exe -ssh -v ubuntu@192.168.1.12 -P 22 -pw ubuntu'
    log.logger.info('ssh execute command:{}'.format(cmd))
    ssh_handle = pexpect.popen_spawn.PopenSpawn(cmd, timeout=timeout)
    exp = ssh_handle.expect(['y/n', 'session'])
    if exp == 0:
        exp1 = execute_cmd_by_ssh(ssh_handle, 'y', prompt=['k-laptop'])
        if exp1 == 0:
            log.logger.info('login success')
            return ssh_handle
    elif exp == 1:
        exp2 = execute_cmd_by_ssh(ssh_handle, '', prompt=['k-laptop'])
        if exp2 == 0:
            log.logger.info('login success')
            return ssh_handle


def execute_cmd_by_ssh(handle, cmd, prompt=['']):
    """
    ssh 命令执行，AC 与AP均可使用此方法，并将结果进行返回；
    :param cmd: 执行的命令；
    :param timeout:设置等待某信息的超时时间，默认为5s;
    :param prompt: 等待的提示符,默认为：>；
    :return: 返回执行消息的返回值,如果执行出现异常，超时等返回None;
    """
    log = gl.get_value('log')
    handle.send(cmd + '\r')
    if len(prompt) > 0:
        exp = handle.expect(prompt)
        log.logger.info(
            handle.before.decode('utf-8').replace('\r', '') + handle.after.decode('utf-8').replace('\r', ''))
        return exp


def ping_to_dut(ssh_handle, ip):
    log = gl.get_value('log')
    exp = execute_cmd_by_ssh(ssh_handle, 'fping ' + ip, prompt=['unreachable', 'alive'])
    if exp == 0:
        log.logger.info(ip + ' can not connected')
        return 0
    elif exp == 1:
        log.logger.info(ip + ' can connected')
        return 1


def ping_connect_dut(sn):
    log = gl.get_value('log')
    flag = 0
    i = 0
    while i <= 5:
        result = os.popen('ping 192.168.1.12 -S 192.168.1.222').read()
        log.logger.info(result)
        i += 1
        if 'TTL' in result:
            flag = 1
            break
    if flag == 1:
        log.logger.info('Connect To DUT SUCCESS')
        return 'ok'
    else:
        log.logger.info('Connect To DUT FAIL')
        return 'fail'

def check_file_md5sum(filepath, username='root'):
    log = gl.get_value('log')
    # log = Logger(sn)
    # gl._init()
    # gl.set_value('log', log)
    ssh_handle = login_product('192.168.1.12', username)
    # ssh_handle = login_ubuntu('192.168.2.183', 10)
    execute_cmd_by_ssh(ssh_handle, 'md5sum ' + filepath)
    exp1 = execute_cmd_by_ssh(ssh_handle, 'pwd', prompt=['/home/k'])

    if exp1 == 0:
        i = ssh_handle.before.decode('utf-8').split('\r\n')[-3]
        md5sum_key = i.split()[1].split('/')[-1] + '_md5sum'
        options = config.options('GAC-A18-01')
        if md5sum_key in options:
            md5sum = config.get('GAC-A18-01', md5sum_key)
        else:
            log.logger.info('no config ' + md5sum_key)
            return 'fail'
        if md5sum == i.split()[0]:
            log.logger.info("{}({})=={}".format(md5sum_key, md5sum, i.split()[0]))
            log.print_log(filepath + ' md5sum check finished')
            return 'ok'
        else:
            return 'fail'


def remove_knows_hosts(sn):
    log = Logger(sn)
    gl._init()
    gl.set_value('log', log)
    ssh_handle = login_product('192.168.1.12', 'ubuntu')
    exp = execute_cmd_by_ssh(ssh_handle, 'sudo rm -rf /root/.ssh', prompt=['password'])
    if exp == 0:
        exp1 = execute_cmd_by_ssh(ssh_handle, 'ubuntu', prompt=['do sync'])
        if exp1 == 0:
            log.print_log('remove knows hosts ok')
            return 'ok'