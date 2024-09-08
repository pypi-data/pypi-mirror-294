import json
import subprocess


def exec_reboot() -> str:
    cmd = ['shutdown', '-r', 'now']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_output, cmd_error = proc.communicate()
    
    if str(proc.returncode) == '0':
        return cmd_output.decode('ascii')
    else:
        return cmd_output.decode('ascii') + '\n' + cmd_error.decode('ascii')


def exec_shutdown() -> str:
    cmd = ['shutdown', '-h', 'now']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_output, cmd_error = proc.communicate()
    
    if str(proc.returncode) == '0':
        return cmd_output.decode('ascii')
    else:
        return cmd_output.decode('ascii') + '\n' + cmd_error.decode('ascii')


def exec_status() -> str:
    #
    cmd = ['mpstat', '-o', 'JSON']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_output, cmd_error = proc.communicate()

    if str(proc.returncode) == '0':
        cpu_stat = json.loads(cmd_output.decode('ascii'))
    else:
        return cmd_output.decode('ascii') + '\n' + cmd_error.decode('ascii')

    report = f'{cpu_stat['sysstat']['hosts'][0]['nodename']}\n'\
                f'{cpu_stat['sysstat']['hosts'][0]['sysname']} '\
                f'{cpu_stat['sysstat']['hosts'][0]['release']} '\
                f'{cpu_stat['sysstat']['hosts'][0]['machine']}\n'\
                f'CPUs num: {cpu_stat['sysstat']['hosts'][0]['number-of-cpus']}\n'\
                f'CPUs load: {"{:.2f}".format(100.00 - cpu_stat['sysstat']['hosts'][0]['statistics'][0]['cpu-load'][0]['idle'])}\n'

    #    
    cmd = ['free', '-m']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_output, cmd_error = proc.communicate()

    if str(proc.returncode) == '0':
        mem_stat = cmd_output.decode('ascii').split()
        for idx, m in enumerate(mem_stat):
            if m == 'Mem:':
                report += f'Mem used: {mem_stat[idx+2]}/{mem_stat[idx+1]}'
                break
    else:
        return cmd_output.decode('ascii') + '\n' + cmd_error.decode('ascii')

    # psutils

    return report


def exec_run(cmd) -> str:
    print(cmd)
    cmd = cmd.split()[1:]
    print(cmd)
    # first /run
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_output, cmd_error = proc.communicate()
    
    if str(proc.returncode) == '0':
        return cmd_output.decode('ascii')
    else:
        return cmd_output.decode('ascii') + '\n' + cmd_error.decode('ascii')


