import socket
import sys
import os
import sqlite3
import easygui as eg

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def receivedata():
    length = connection.recv(16)
    length = int(length)
    connection.sendall("go")
    buff=''
    while len(buff) < length:
        buff += connection.recv( length - len(buff) )
    return buff

def senddata(string):
    print "establishing terms..."	
    # send size of transmission
    length = len(string)
    connection.sendall(str(length))
    # wait for their go
    data = connection.recv(16)
    print "established."
    if data == "go":
        print "sending data..."
        connection.sendall(string)
        print "sent."
    else:
        print "abort."

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (get_lan_ip(), 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(10)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'verifying connection from', client_address
        # verify connection
        
        data = connection.recv(250)
        if data == "gl":
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            flist = "AVALIZED FILES:"
            for row in cursor.execute("SELECT * FROM filelist"):
                flist += "\n" + str(row[0]) + " - " + str(row[1])
            senddata(flist)
        elif data.startswith("gf*"):
            parts = data.split("*", 1)
            fil = parts[1]
            # query data.db to find full path of file.
            elephant = open(fil)
            content = file.read(elephant)
            senddata(content)
        elif data.startswith("sf*"):
            parts = data.split("*", 1)
            path, fil = os.path.split(parts[1])
            print client_address, " wants to send", fil, "to you."
            if eg.ynbox("someone wants to send " + fil + " to you.", "transmission request"):
                lfil = eg.filesavebox(msg=None, title=None, default=fil, filetypes=None)
                if lfil == "None":
                    print "abort."
                else:
                    connection.sendall("y")
                    data = receivedata()
                    print "transmission completed."
                    lf = open(lfil, 'wb')
                    lf.write(data)
                    lf.close()
            else: 
                connection.sendall("n")
                print "abort"
        else:
            print 'no more data from', client_address
            break
            
    finally:
        connection.close()
