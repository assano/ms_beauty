# coding: utf-8

import socket
import main

HOST = ''
PORT = 9200

# Configure Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
text_content = '''HTTP/1.0 200 OK
Server: python
Date: Fri, 01 Aug 2014 06:44:11 GMT
Content-Type: application/json

'''
#s.listen(1)
#conn,addr = s.accept()
#
#print 'Connected by',addr
#
#data = conn.rev(1024)
#conn.sendall(data)

#conn.close()

while True:
    s.listen(3)
    conn, addr = s.accept()
    res = conn.recv(1024)
    method = res.split(' ')[0]
    f = open('2.out','w+')
    f.write(res)
    if method == 'GET':
        f.write(res)
        print res.split(' ')[1]
        req = res.split(' ')[1]
        a = 0
        i = 0
        l = len(req)
        while i<l:
            if req[i]=='=':
                i += 1
                while i<l:
                    if ord(req[i])>=ord('0') and ord(req[i])<=ord('9'):
                        a = a*10L+int(req[i])
                    else:
                        break
                    i += 1
                break
            i += 1
        b = 0
        while i<l:
            if req[i]=='=':
                i +=1
                while i<l:
                    if ord(req[i]) >=ord('0') and ord(req[i])<=ord('9'):
                        b = b*10L+int(req[i])
                    else:
                        break
                    i +=1
                break
            i += 1
        print a
        print b
        conn.sendall(text_content+main.CalcAllPath(a,b))
    f.close()            
    #f.flush()
    conn.close()
