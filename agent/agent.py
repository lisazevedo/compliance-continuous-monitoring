import os, subprocess, shlex, psutil

def get_host_ip():
    bashCommand = shlex.split("hostname -I")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    host, error = process.communicate()
    return host.decode("utf-8")

def get_so_name():
    bashCommand = shlex.split("uname -sn")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_name, error = process.communicate()
    return so_name.decode("utf-8")

def get_so_version():
    bashCommand = shlex.split("uname -r")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_version, error = process.communicate()
    return so_version.decode("utf-8")

def get_users():
    bashCommand = shlex.split("who")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    users = []

    for line in output.splitlines():
        users.append(line.decode("utf-8").split(' ')[0])
    
    return users

def get_pid():
    users = os.popen("ps aux | awk '{print $1}'")
    pid = os.popen("ps aux | awk '{print $2}'")
    outputUsers = list(users.read().split("\n"))
    outputPid = list(pid.read().split("\n"))
    users.close()
    pid.close()

    res = {}
    for key in outputPid:
        for value in outputUsers:
            res[key] = value
            outputUsers.remove(value)
            break
    
    res.popitem()  
    res.pop('PID')
    
    return res

def get_usage_cpu():
    return psutil.cpu_percent(2)
        
if __name__ == '__main__':
    get_usage_cpu()