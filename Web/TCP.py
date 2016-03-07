# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 23:00:18 2016

@author: T800GHB

This file will demostrate basic TCP operation.
"""
import socket

def run_demo():
    """
    This demo will show how to establish a TCP connection and 
    achive some web page.
    """
    #Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Establish a connection
    s.connect(('www.sina.com.cn', 80))
    #Send request
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    #Receive data
    buffer = []
    while True:
        #Set max size of reception for recv function.
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    #Bind a character
    data = b''.join(buffer)
    #Destroy connection
    s.close()
    #Separate HTTP header and web page.
    header, html = data.split(b'\r\n\r\n',1)
    print(header.decode('utf-8'))
    #Save html content to file.
    with open('sina.html','wb') as f:
        f.write(html)
    
