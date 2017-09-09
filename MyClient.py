#encoding=gbk

import socket
import json

host_name = '127.0.0.1'
port_num = 8888

if __name__ == '__main__':
    try:
        sk = socket.socket()
        sk.connect((host_name, port_num))

        jdata = ['command', 'sendinfo']
        data = json.dumps(jdata)
        sk.sendall(data)
        if sk.recv(1024) != 'success':
            pass

        jdata = ['data', {'name':'lxj', 'sex': 'male', 'age': 26}]
        data = json.dumps(jdata)
        sk.sendall(data)
        if sk.recv(1024) != 'success':
            pass

        jdata = ['end']
        data = json.dumps(jdata)
        sk.sendall(data)


    except Exception as e:
        print 'Exception:', e