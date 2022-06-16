import os, subprocess, shlex, psutil, sys


def get_host_ip():
    bashCommand = os.popen("hostname -I | awk '{print $1}'")
    host = bashCommand.read()
    bashCommand.close()

    return host.strip('\n')

def get_so_name():
    bashCommand = shlex.split("uname -sn")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_name, error = process.communicate()

    obj = {
        'ip': get_host_ip(),
        'so_name': so_name.decode("utf-8").strip('\n')
    }
    return obj

def get_so_version():
    bashCommand = shlex.split("uname -r")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    so_version, error = process.communicate()

    obj = {
        'ip': get_host_ip(),
        'so_version': so_version.decode("utf-8").strip('\n')
    }

    return obj

def get_users():
    bashCommand = shlex.split("who")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    users = []

    for line in output.splitlines():
        users.append(line.decode("utf-8").split(' ')[0])
    
    obj = {
        'host': get_host_ip(),
        'users': users
    }

    return obj
    
def get_pid():
    users = os.popen("ps aux | awk '{print $1}'")
    pid = os.popen("ps aux | awk '{print $2}'")
    outputUsers = list(users.read().split("\n"))
    outputPid = list(pid.read().split("\n"))
    users.close()
    pid.close()
    processes = []
    for key in outputPid:
        for value in outputUsers:
            obj = {
                "pid": key,
                "user": value
            }
            processes.append(obj)
            outputUsers.remove(value)
            break
    
    processes.pop(0)
    del processes[-1]
    
    obj = {
        'host': get_host_ip(),
        'processes': processes
    }

    return obj

def get_cpu_usage():
    
    obj = {
        'host': get_host_ip(),
        'cpu_usage': str(psutil.cpu_percent(2))
    }
    return obj
        
if __name__ == '__main__':

    if sys.argv[1] == "so-name":
        print(get_so_name())
    elif sys.argv[1] == "ps":
        print(get_pid())
    elif sys.argv[1] == "users":
        print(get_users())
    elif sys.argv[1] == "so-version":
        print(get_so_version())
    elif sys.argv[1] == "cpu":
        print(get_cpu_usage())
    else:
        print("\ninvalid option!\n")
        print("python3 "+sys.argv[0]+" so-name    -   Send SO name")
        print("python3 "+sys.argv[0]+" ps         -   Send processes")
        print("python3 "+sys.argv[0]+" users      -   Send online users")
        print("python3 "+sys.argv[0]+" so-version -   Send SO version")
        print("python3 "+sys.argv[0]+" cpu        -   Send CPU usage\n")