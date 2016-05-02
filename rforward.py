def main():
    options, server, remote = parse_options()
    password = None
    if options.readpass:
# 2 ssh client connection
        password = getpass('Enter SSH password: ')
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    verbose('Connecting to SSH host %s:%d ...' % (server[0], server[1]))
    try:
        client.connect(server[0], server[1], username=options.user,
        key_filename=options.keyfile,
        look_for_keys= options.look_for_keys, password= password)
    except Exception as ex:
        print ('*** Failed to connect to %s:%d %r' % (server[0], server[1], ex))
        sys.exit(1)
    verbose ('Now forwarding remote port %d to %s:%d ...' % (options.port,
    remote[0], remote[1]))
# 3
    try:
        reverse_forward_tunnel(options.port, remote[0], remote[1],
        client.get_transport())
    except KeyboardInterrupt:
        print ('C-c: Port forwarding stopped.')
        sys.exit(0)
def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    # forward TCP connection from port
    transport.request_port_forward('', server_port)
    while True:
        # SSH server and start up a new transport channel
        channel = transport.accept(1000)
        if channel is None:
            continue
        #channel over and handler
        thr = threading.Thread(target= handler, args=(channel, remote_host,
        remote_port))
        thr.setDaemon(True)
        thr.start()
def handler(channel, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as ex:
        verbose('Forwarding request to %s:%d failed: %r' % (host, port, ex))
        return
    verbose('Connected! Tunnel open %r -> %r -> %r' % (channel.origin_addr,
    channel.getpeername(),(host, port)))
    # data sent and received
    while True:
        r, w, x = select.select([sock, channel], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            channel.send(data)
        if channel in r:
            data = recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    channel.close()
    sock.close()
    verbose('Tunnel closed from %r' % (channel.origin_addr,))
