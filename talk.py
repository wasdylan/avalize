import socket
import sys
import sqlite3
import os
import easygui as eg

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
    fil = sys.argv[2]
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    if fil.isdigit() == True:
        query = "DELETE FROM filelist WHERE id='%s'" % fil
        cursor.execute(query)
        conn.commit()
    else:
        query = "DELETE FROM filelist WHERE filepath LIKE '%"+fil+"%'"
        cursor.execute(query)
        conn.commit()
    conn.close()
elif req == "mylist":
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    flist = "AVALIZED FILES:"
    for row in cursor.execute("SELECT * FROM filelist"):
        flist += "\n" + str(row[0]) + " - " + str(row[1])
    print flist
elif req == "sendfile" or "getfile" or "getlist":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sys.argv[2], 10006)
    sock.connect(server_address)
    try:
        if req == "getfile":
            rfil = sys.argv[3]
            lfil = eg.filesavebox(msg=None, title=None, default=rfil, filetypes=None)
            if lfil == "None":
                print "abort."
            else:
                sock.sendall("gf*" + rfil)
                data = receivedata()
                lf = open(lfil, 'wb')
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
                print "peer rejected transmission, aborting."
    finally:
        sock.close()
