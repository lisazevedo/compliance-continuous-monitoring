import sys
import subprocess 
import shlex

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
    bashCommand = shlex.split("ps aux")
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    users = []

    for line in output.splitlines():
        users.append(line.decode("utf-8").split(' ')[0])
    
    return users

if __name__ == '__main__':
    print(get_pid())