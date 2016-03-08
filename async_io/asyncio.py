# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 23:15:09 2016

@author: T800GHB

This file will demostrate how to use asynchronous io.
asyncio was introduced by python3.4 as built-in model.
"""

import asyncio
import threading

"""
Use @asyncio.coroutine could label generator as coroutine type.
yield from could call other generator.
"""
@asyncio.coroutine
def execute():
    print('Execute once %s' %threading.current_thread())
    """
    When execute yield from, main thread will not wait for it.
    Main thread will do other job until yield from finished, then continue
    rest job of this coroutine.
    """
    yield from asyncio.sleep(3)
    print('Execute again %s' %threading.current_thread())
    
def run_demo_sleep():
    """
    get_event_loop function will create a eventloop reference, then wen need 
    to execute coroutine onto this eventloop.
    """
    loop = asyncio.get_event_loop()
    """
    Use asyncio on wrapped tasks could run parallel.
    wait function will wiat for futures.
    """
    tasks = [execute(), execute()]
    loop.run_until_complete(asyncio.wait(tasks))
    """
    There are some proble.
    When i close current event loop, event loop could not be used 
    once again.
    If restart current python envirenment, it could be used normally.
    I think it should not be closed, because it is a reference.
    """
    loop.close()
    
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()
    
def run_demo_wget():
    loop_wget = asyncio.get_event_loop()
    tasks = [wget(host) for host in
            ['www.sina.com.cn','www.sohu.com','www.163.com']]
    loop_wget.run_until_complete(asyncio.wait(tasks))
    loop_wget.close()
