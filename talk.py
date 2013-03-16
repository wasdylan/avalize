import socket
import sys
import sqlite3
import os

def receivedata():
    length = sock.recv(16)
    length = int(length)
    sock.sendall("go")
    buff=''
    while len(buff) < length:
        buff += sock.recv( length - len(buff) )
    return buff

def senddata(string):
    print "establishing terms..."
    length = len(string)
    sock.sendall(str(length))
    data = sock.recv(16)
    print "established."
    if data == "go":
        print "sending data..."
        sock.sendall(string)
        print "sent."
    else:
        print "abort."

req = sys.argv[1]

if req == "avalize":
    fil = sys.argv[2]
    abspath = os.path.abspath(fil)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO filelist (filepath) VALUES ('" + abspath + "')")
    conn.commit()
    conn.close()
elif req == "devalize":
    print "haha"
elif req == "sendfile" or "getfile" or "getlist":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sys.argv[2], 10001)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        if req == "getfile":
            rfil = sys.argv[3]
            sock.sendall("gf*" + rfil)
            data = receivedata()
            lf = open("Fade.mp3", 'wb')
            lf.write(data)
            lf.close()
        elif req == "getlist":
            sock.sendall("gl")
            data = receivedata()
            print data
        elif req == "sendfile":
            fil = sys.argv[3]
            print "requesting manual transmission... "
            sock.sendall("sf*" + fil)
            confirmation = sock.recv(16)
            if confirmation == "y":
                print "peer accepted transmission."
                elephant = open(fil)
                content = file.read(elephant)
                senddata(content)
            else:
                sys.stdout.write("peer rejected transmission, aborting.\n") 
    finally:
        sock.close()
