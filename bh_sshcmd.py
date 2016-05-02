import threading
import paramiko
import subprocess
# pivot with BHNet to handle encrypt personal traffic to avoid detection.
# Using SSH
def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, passord=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return
ssh_command('192.168.100.131','khanh', 'pip_python','id')
