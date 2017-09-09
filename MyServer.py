#encoding=gbk

import sys
import socket
import json
import threading
import time

host_name = '127.0.0.1'
port_num = 8888
isStart = False
mutex = threading.Lock()

def DoSendInfo(conn):
    jdata = conn.recv(1024)
    data = json.loads(jdata)
    while data[0] != 'end':
        for key in data[1].keys():
            print key + ':' + str(data[1][key])
        time.sleep(3)
        conn.send('success')
        jdata = conn.recv(1024)
        data = json.loads(jdata)


def RunTask(conn, address):
    print '接到客户端连接：' + address[0] + ':' + str(address[1])
    jdata = conn.recv(1024)
    data = json.loads(jdata)

    if data[0] == 'command':
        print 'command:' + data[1]
        conn.send('success')
        if address[0] == host_name and data[1] == 'stop':
            global isStart, mutex
            if mutex.acquire():
                isStart = False
                mutex.release()
        elif data[1] == 'sendinfo':
            DoSendInfo(conn)

    conn.close()




def StartServer():
    try:
        global isStart, mutex
        if mutex.acquire():
            isStart = True
            mutex.release()
        sk = socket.socket()
        sk.bind((host_name, port_num))
        sk.listen(5)
        print 'listening......'
        mutex.acquire()
        while isStart:
            mutex.release()
            conn, address = sk.accept()
            t = threading.Thread(target=RunTask, args=(conn, address))
            t.setDaemon(True)
            t.start()
            time.sleep(1)
            mutex.acquire()
            #RunTask(conn, address)
        sk.close()

    except Exception as e:
        print 'Exception:', e
    pass

def StopServer():
    jdata = ['command','stop']
    data = json.dumps(jdata)
    sk = socket.socket()
    sk.connect((host_name,port_num))
    sk.sendall(data)
    sk.close()
    pass

if __name__ == '__main__':
    if 2 > len(sys.argv):
        print '参数不合法'
        pass
    for parm in sys.argv:
        if parm == 'start':
            print 'host_name:' + host_name
            print 'host_num:' + str(port_num)
            print 'start server......'
            StartServer()
            pass
        elif parm == 'stop':
            StopServer()
            pass
