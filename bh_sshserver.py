import socket
import paramiko
import threading
import sys
#using the key from the paramiko file
host_key = paramiko.RSAkey(filename= :'test_rsa.key')
# 2 configure authentication
class Server(paramiko.ServerInterface):
    def _init(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanId):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if(username == 'khanh') and (password = 'pip_python'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])
# 3 listener
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSERADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print '[+] Listening for connection ...'
        client, addr = sock.accept()
    except Exception, ex:
        print '[-] Listen failed: ' + str(ex)
        sys.exit(1)
    print '[+] Got a connection!'
# 4 if client is authenticated
    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()
        try:
            bhSession.start_server(server = server)
        except paramiko.SSHException, e:
            print '[-] SSH negotiation failed.'
        channel = bhSession.accept(20)
# 5 send for connection
        print '[+] Authenticated!'
        print channel.recv(1024)
        channel.send('Welcome To bh_ssh')
# 6 command typed to ssh
        while True:
            try:
                command = raw_input("Enter command: ").strip('\n')
                if command != 'exit':
                    channel.send(command)
                    print channel.recv(1024) + '\n'
                else:
                    channel.send('exit')
                    print 'exiting'
                    bhSession.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                bhSession.close()
    except Exception, exp:
        print '[-] Caught exception: ' + str(exp)
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)
