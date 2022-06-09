import os, subprocess, shlex, psutil, sys

def get_host_ip():
    bashCommand = os.popen("hostname -I | awk '{print $1}'")
    host = bashCommand.read()
    bashCommand.close()

    return host

def get_so_name():
    bashCommand = shlex.split("uname -sn")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_name, error = process.communicate()

    return get_host_ip(), so_name.decode("utf-8")

def get_so_version():
    bashCommand = shlex.split("uname -r")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_version, error = process.communicate()

    return get_host_ip(), so_version.decode("utf-8")

def get_users():
    bashCommand = shlex.split("who")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    users = []

    for line in output.splitlines():
        users.append(line.decode("utf-8").split(' ')[0])
    
    return get_host_ip(), users

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
    
    return get_host_ip(), res

def get_usage_cpu():
    return get_host_ip(), psutil.cpu_percent(2)
        
if __name__ == '__main__':

    if sys.argv[1] == "so-name":
        get_so_name()
    elif sys.argv[1] == "ps":
        get_pid()
    elif sys.argv[1] == "users":
        get_users()
    elif sys.argv[1] == "so-version":
        get_so_version()
    elif sys.argv[1] == "cpu":
        get_usage_cpu()
    else:
        print("\ninvalid option!\n")
        print("python3 "+sys.argv[0]+" so-name    -   Send SO name")
        print("python3 "+sys.argv[0]+" ps         -   Send processes")
        print("python3 "+sys.argv[0]+" users      -   Send online users")
        print("python3 "+sys.argv[0]+" so-version -   Send SO version")
        print("python3 "+sys.argv[0]+" cpu        -   Send CPU usage")